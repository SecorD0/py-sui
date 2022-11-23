import logging
from typing import Optional

import requests
from pretty_utils.type_functions.lists import split_list

from py_sui import exceptions
from py_sui.models import Balance, Coin, Nft, ObjectID
from py_sui.rpc_methods import RPC
from py_sui.utils import parse_type


class Wallet:
    def __init__(self, client):
        self.client = client
        self.req_get: requests.get = self.client.session.get
        self.req_post: requests.post = self.client.session.post

    def balance(self, address: Optional[str] = None) -> Balance:
        balance = Balance(tokens={}, nfts={}, misc={})
        try:
            if not address:
                address = self.client.account.address

            response = RPC.getObjectsOwnedByAddress(client=self.client, address=address)
            queries = [RPC.getObject(client=self.client, object_id=obj['objectId'], get_json=True) for obj in
                       response['result']]
            query_list = split_list(queries, 200)
            objs = []
            for json_data in query_list:
                objs += RPC.send_request(client=self.client, json_data=json_data)

            for obj in objs:
                obj_id = obj['result']['details']['reference']['objectId']
                obj_data = obj['result']['details']['data']
                obj_type = parse_type(obj_data['type'])
                obj_fields = obj_data['fields']

                if obj_type.type == 'coin':
                    obj_id = ObjectID(id=obj_id, amount=obj_fields['balance'])
                    if obj_type.name == 'sui':
                        if balance.coin:
                            balance.coin.balance += obj_fields['balance']
                            balance.coin.object_ids.append(obj_id)

                        else:
                            balance.coin = Coin(name=obj_type.name, symbol=obj_type.symbol,
                                                package_id=obj_type.package_id,
                                                balance=obj_fields['balance'], object_ids=[obj_id])

                    else:
                        if obj_type.name in balance.tokens:
                            coin = balance.tokens[obj_type.name]
                            coin.balance += obj_fields['balance']
                            coin.object_ids.append(obj_id)

                        else:
                            balance.tokens[obj_type.name] = Coin(name=obj_type.name, symbol=obj_type.symbol,
                                                                 package_id=obj_type.package_id,
                                                                 balance=obj_fields['balance'], object_ids=[obj_id])

                elif 'nft' in obj_type.raw_type.lower():
                    balance.nfts[obj_id] = Nft(name=obj_fields['name'], description=obj_fields['description'],
                                               image_url=obj_fields['url'], object_id=obj_id)

                else:
                    balance.misc[obj_id] = obj_data

        except:
            logging.exception('balance')

        finally:
            return balance

    def find_object_for_gas(self, gas_budget: int = 10_000, balance: Optional[Balance] = None) -> Optional[str]:
        if not balance:
            coin = None
            response = RPC.getObjectsOwnedByAddress(client=self.client, address=self.client.account.address)
            queries = [RPC.getObject(client=self.client, object_id=obj['objectId'], get_json=True) for obj in
                       response['result']]
            query_list = split_list(queries, 200)
            objs = []
            for json_data in query_list:
                objs += RPC.send_request(client=self.client, json_data=json_data)

            for obj in objs:
                obj_id = obj['result']['details']['reference']['objectId']
                obj_data = obj['result']['details']['data']
                obj_type = parse_type(obj_data['type'])
                obj_fields = obj_data['fields']
                if obj_type.type == 'coin' and obj_type.name == 'sui':
                    obj_id = ObjectID(id=obj_id, amount=obj_fields['balance'])
                    if coin:
                        coin.balance += obj_fields['balance']
                        coin.object_ids.append(obj_id)

                    else:
                        coin = Coin(name=obj_type.name, symbol=obj_type.symbol, package_id=obj_type.package_id,
                                    balance=obj_fields['balance'], object_ids=[obj_id])

        else:
            coin = balance.coin

        sorted_objects = sorted(coin.object_ids, key=lambda obj: obj.amount)
        for object_id in sorted_objects:
            if object_id.amount >= gas_budget:
                return object_id.id

    def request_coins_from_faucet(self) -> Optional[dict]:
        if self.client.network.faucet:
            json_data = {
                "FixedAmountRequest": {"recipient": self.client.account.address}
            }
            response = self.client.session.post(self.client.network.faucet, json=json_data)

            if response.status_code <= 201:
                return response.json()

            else:
                raise exceptions.RPCException(
                    f'The RPC was called with an error {response.status_code}! Details: {response.text}')

        else:
            raise exceptions.FaucetException("You didn't specify the faucet URL!")