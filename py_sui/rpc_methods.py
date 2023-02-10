import uuid
from typing import Optional, List, Union

from py_sui import exceptions, types
from py_sui.models import ObjectType


class RPC:
    version = '0.26.0'

    @staticmethod
    def make_json(method: str, params: Optional[list] = None, request_id: Optional[str] = None):
        return {
            "jsonrpc": "2.0",
            "method": method,
            "params": params or [],
            "id": request_id or str(uuid.uuid4()),
        }

    @staticmethod
    def send_request(client, json_data: Union[dict, list]) -> Optional[dict]:
        response = client.session.post(client.network.rpc, json=json_data)
        if response.status_code <= 201:
            json_dict = response.json()
            if 'error' in json_dict:
                error = json_dict['error']
                raise exceptions.RPCException(response=response, code=error['code'], message=error['message'])

            return json_dict

        raise exceptions.RPCException(response=response)

    @staticmethod
    def batchTransaction(client, signer: types.SuiAddress,
                         single_transaction_params: List[types.RPCTransactionRequestParams],
                         gas: Optional[types.ObjectID] = None, gas_budget: int = 1_000,
                         get_json: bool = False) -> Optional[Union[dict, list]]:
        params = [signer, single_transaction_params, gas, gas_budget]
        json_data = RPC.make_json(method='sui_batchTransaction', params=params)
        if get_json:
            return json_data

        return RPC.send_request(client=client, json_data=json_data)

    @staticmethod
    def devInspectTransaction(client, sender_address: types.SuiAddress, tx_bytes: types.Base64, gas_price: int,
                              epoch: int, get_json: bool = False) -> Optional[Union[dict, list]]:
        params = [sender_address, tx_bytes, gas_price, epoch]
        json_data = RPC.make_json(method='sui_devInspectTransaction', params=params)
        if get_json:
            return json_data

        return RPC.send_request(client=client, json_data=json_data)

    @staticmethod
    def dryRunTransaction(client, tx_bytes: types.Base64, get_json: bool = False) -> Optional[Union[dict, list]]:
        params = [tx_bytes]
        json_data = RPC.make_json(method='sui_dryRunTransaction', params=params)
        if get_json:
            return json_data

        return RPC.send_request(client=client, json_data=json_data)

    @staticmethod
    def executeTransaction(client, tx_bytes: types.Base64, sig_scheme: types.SignatureScheme,
                           signature: types.Base64, pub_key: types.Base64,
                           request_type: types.ExecuteTransactionRequestType,
                           get_json: bool = False) -> Optional[Union[dict, list]]:
        params = [tx_bytes, sig_scheme, signature, pub_key, request_type]
        json_data = RPC.make_json(method='sui_executeTransaction', params=params)
        if get_json:
            return json_data

        return RPC.send_request(client=client, json_data=json_data)

    @staticmethod
    def executeTransactionSerializedSig(client, tx_bytes: types.Base64, signature: types.Base64,
                                        request_type: types.ExecuteTransactionRequestType,
                                        get_json: bool = False) -> Optional[Union[dict, list]]:
        params = [tx_bytes, signature, request_type]
        json_data = RPC.make_json(method='sui_executeTransactionSerializedSig', params=params)
        if get_json:
            return json_data

        return RPC.send_request(client=client, json_data=json_data)

    @staticmethod
    def getAllBalances(client, owner: types.SuiAddress, get_json: bool = False) -> Optional[Union[dict, list]]:
        params = [owner]
        json_data = RPC.make_json(method='sui_getAllBalances', params=params)
        if get_json:
            return json_data

        return RPC.send_request(client=client, json_data=json_data)

    @staticmethod
    def getAllCoins(client, owner: types.SuiAddress, cursor: types.ObjectID,
                    limit: Optional[int], get_json: bool = False) -> Optional[Union[dict, list]]:
        params = [owner, cursor, limit]
        json_data = RPC.make_json(method='sui_getAllCoins', params=params)
        if get_json:
            return json_data

        return RPC.send_request(client=client, json_data=json_data)

    @staticmethod
    def getBalance(client, owner: types.SuiAddress, coin_type: Union[str, ObjectType],
                   get_json: bool = False) -> Optional[Union[dict, list]]:
        params = [owner, coin_type.raw_type if isinstance(coin_type, ObjectType) else coin_type]
        json_data = RPC.make_json(method='sui_getBalance', params=params)
        if get_json:
            return json_data

        return RPC.send_request(client=client, json_data=json_data)

    @staticmethod
    def getCheckpointContents(client, sequence_number: int, get_json: bool = False) -> Optional[Union[dict, list]]:
        params = [sequence_number]
        json_data = RPC.make_json(method='sui_getCheckpointContents', params=params)
        if get_json:
            return json_data

        return RPC.send_request(client=client, json_data=json_data)

    @staticmethod
    def getCheckpointContentsByDigest(client, digest: types.CheckpointContentsDigest,
                                      get_json: bool = False) -> Optional[Union[dict, list]]:
        params = [digest]
        json_data = RPC.make_json(method='sui_getCheckpointContentsByDigest', params=params)
        if get_json:
            return json_data

        return RPC.send_request(client=client, json_data=json_data)

    @staticmethod
    def getCheckpointSummary(client, sequence_number: int, get_json: bool = False) -> Optional[Union[dict, list]]:
        params = [sequence_number]
        json_data = RPC.make_json(method='sui_getCheckpointSummary', params=params)
        if get_json:
            return json_data

        return RPC.send_request(client=client, json_data=json_data)

    @staticmethod
    def getCheckpointSummaryByDigest(client, digest: types.CheckpointDigest,
                                     get_json: bool = False) -> Optional[Union[dict, list]]:
        params = [digest]
        json_data = RPC.make_json(method='sui_getCheckpointSummaryByDigest', params=params)
        if get_json:
            return json_data

        return RPC.send_request(client=client, json_data=json_data)

    @staticmethod
    def getCoinMetadata(client, coin_type: Union[str, ObjectType],
                        get_json: bool = False) -> Optional[Union[dict, list]]:
        params = [coin_type.raw_type if isinstance(coin_type, ObjectType) else coin_type]
        json_data = RPC.make_json(method='sui_getCoinMetadata', params=params)
        if get_json:
            return json_data

        return RPC.send_request(client=client, json_data=json_data)

    @staticmethod
    def getCoins(client, owner: types.SuiAddress, coin_type: Union[str, ObjectType], cursor: types.ObjectID,
                 limit: Optional[int], get_json: bool = False) -> Optional[Union[dict, list]]:
        params = [owner, coin_type.raw_type if isinstance(coin_type, ObjectType) else coin_type, cursor, limit]
        json_data = RPC.make_json(method='sui_getCoins', params=params)
        if get_json:
            return json_data

        return RPC.send_request(client=client, json_data=json_data)

    @staticmethod
    def getCommitteeInfo(client, epoch: int, get_json: bool = False) -> Optional[Union[dict, list]]:
        params = [epoch]
        json_data = RPC.make_json(method='sui_getCommitteeInfo', params=params)
        if get_json:
            return json_data

        return RPC.send_request(client=client, json_data=json_data)

    @staticmethod
    def getDelegatedStakes(client, owner: types.SuiAddress, get_json: bool = False) -> Optional[Union[dict, list]]:
        params = [owner]
        json_data = RPC.make_json(method='sui_getDelegatedStakes', params=params)
        if get_json:
            return json_data

        return RPC.send_request(client=client, json_data=json_data)

    @staticmethod
    def getDynamicFieldObject(client, parent_object_id: types.ObjectID, name: str,
                              get_json: bool = False) -> Optional[Union[dict, list]]:
        params = [parent_object_id, name]
        json_data = RPC.make_json(method='sui_getDynamicFieldObject', params=params)
        if get_json:
            return json_data

        return RPC.send_request(client=client, json_data=json_data)

    @staticmethod
    def getDynamicFields(client, parent_object_id: types.ObjectID, cursor: types.ObjectID,
                         limit: Optional[int], get_json: bool = False) -> Optional[Union[dict, list]]:
        params = [parent_object_id, cursor, limit]
        json_data = RPC.make_json(method='sui_getDynamicFields', params=params)
        if get_json:
            return json_data

        return RPC.send_request(client=client, json_data=json_data)

    @staticmethod
    def getEvents(client, query: types.EventQuery, cursor: types.EventID, limit: int,
                  descending_order: bool = False, get_json: bool = False) -> Optional[Union[dict, list]]:
        params = [query, cursor, limit, descending_order]
        json_data = RPC.make_json(method='sui_getEvents', params=params)
        if get_json:
            return json_data

        return RPC.send_request(client=client, json_data=json_data)

    @staticmethod
    def getLatestCheckpointSequenceNumber(client, get_json: bool = False) -> Optional[Union[dict, list]]:
        json_data = RPC.make_json(method='sui_getLatestCheckpointSequenceNumber')
        if get_json:
            return json_data

        return RPC.send_request(client=client, json_data=json_data)

    @staticmethod
    def getMoveFunctionArgTypes(client, package: types.ObjectID, module: str, function: str,
                                get_json: bool = False) -> Optional[Union[dict, list]]:
        params = [package, module, function]
        json_data = RPC.make_json(method='sui_getMoveFunctionArgTypes', params=params)
        if get_json:
            return json_data

        return RPC.send_request(client=client, json_data=json_data)

    @staticmethod
    def getNormalizedMoveFunction(client, package: types.ObjectID, module: str, function: str,
                                  get_json: bool = False) -> Optional[Union[dict, list]]:
        params = [package, module, function]
        json_data = RPC.make_json(method='sui_getNormalizedMoveFunction', params=params)
        if get_json:
            return json_data

        return RPC.send_request(client=client, json_data=json_data)

    @staticmethod
    def getNormalizedMoveModule(client, package: types.ObjectID, module_name: str,
                                get_json: bool = False) -> Optional[Union[dict, list]]:
        params = [package, module_name]
        json_data = RPC.make_json(method='sui_getNormalizedMoveModule', params=params)
        if get_json:
            return json_data

        return RPC.send_request(client=client, json_data=json_data)

    @staticmethod
    def getNormalizedMoveModulesByPackage(client, package: types.ObjectID,
                                          get_json: bool = False) -> Optional[Union[dict, list]]:
        params = [package]
        json_data = RPC.make_json(method='sui_getNormalizedMoveModulesByPackage', params=params)
        if get_json:
            return json_data

        return RPC.send_request(client=client, json_data=json_data)

    @staticmethod
    def getNormalizedMoveStruct(client, package: types.ObjectID, module_name: str,
                                struct_name: str, get_json: bool = False) -> Optional[Union[dict, list]]:
        params = [package, module_name, struct_name]
        json_data = RPC.make_json(method='sui_getNormalizedMoveStruct', params=params)
        if get_json:
            return json_data

        return RPC.send_request(client=client, json_data=json_data)

    @staticmethod
    def getObject(client, object_id: types.ObjectID, get_json: bool = False) -> Optional[Union[dict, list]]:
        params = [object_id]
        json_data = RPC.make_json(method='sui_getObject', params=params)
        if get_json:
            return json_data

        return RPC.send_request(client=client, json_data=json_data)

    @staticmethod
    def getObjectsOwnedByAddress(client, address: types.SuiAddress,
                                 get_json: bool = False) -> Optional[Union[dict, list]]:
        params = [address]
        json_data = RPC.make_json(method='sui_getObjectsOwnedByAddress', params=params)
        if get_json:
            return json_data

        return RPC.send_request(client=client, json_data=json_data)

    @staticmethod
    def getObjectsOwnedByObject(client, object_id: types.ObjectID,
                                get_json: bool = False) -> Optional[Union[dict, list]]:
        params = [object_id]
        json_data = RPC.make_json(method='sui_getObjectsOwnedByObject', params=params)
        if get_json:
            return json_data

        return RPC.send_request(client=client, json_data=json_data)

    @staticmethod
    def getRawObject(client, object_id: types.ObjectID, get_json: bool = False) -> Optional[Union[dict, list]]:
        params = [object_id]
        json_data = RPC.make_json(method='sui_getRawObject', params=params)
        if get_json:
            return json_data

        return RPC.send_request(client=client, json_data=json_data)

    @staticmethod
    def getReferenceGasPrice(client, get_json: bool = False) -> Optional[Union[dict, list]]:
        json_data = RPC.make_json(method='sui_getReferenceGasPrice')
        if get_json:
            return json_data

        return RPC.send_request(client=client, json_data=json_data)

    @staticmethod
    def getSuiSystemState(client, get_json: bool = False) -> Optional[Union[dict, list]]:
        json_data = RPC.make_json(method='sui_getSuiSystemState')
        if get_json:
            return json_data

        return RPC.send_request(client=client, json_data=json_data)

    @staticmethod
    def getTotalSupply(client, coin_type: Union[str, ObjectType],
                       get_json: bool = False) -> Optional[Union[dict, list]]:
        params = [coin_type.raw_type if isinstance(coin_type, ObjectType) else coin_type]
        json_data = RPC.make_json(method='sui_getTotalSupply', params=params)
        if get_json:
            return json_data

        return RPC.send_request(client=client, json_data=json_data)

    @staticmethod
    def getTotalTransactionNumber(client, get_json: bool = False) -> Optional[Union[dict, list]]:
        json_data = RPC.make_json(method='sui_getTotalTransactionNumber')
        if get_json:
            return json_data

        return RPC.send_request(client=client, json_data=json_data)

    @staticmethod
    def getTransaction(client, digest: types.TransactionDigest, get_json: bool = False) -> Optional[Union[dict, list]]:
        params = [digest]
        json_data = RPC.make_json(method='sui_getTransaction', params=params)
        if get_json:
            return json_data

        return RPC.send_request(client=client, json_data=json_data)

    @staticmethod
    def getTransactionAuthSigners(client, digest: types.TransactionDigest,
                                  get_json: bool = False) -> Optional[Union[dict, list]]:
        params = [digest]
        json_data = RPC.make_json(method='sui_getTransactionAuthSigners', params=params)
        if get_json:
            return json_data

        return RPC.send_request(client=client, json_data=json_data)

    @staticmethod
    def getTransactions(client, query: types.TransactionQuery, cursor: Optional[types.TransactionDigest],
                        limit: Optional[int], descending_order: bool = False,
                        get_json: bool = False) -> Optional[Union[dict, list]]:
        params = [query, cursor, limit, descending_order]
        json_data = RPC.make_json(method='sui_getTransactions', params=params)
        if get_json:
            return json_data

        return RPC.send_request(client=client, json_data=json_data)

    @staticmethod
    def getTransactionsInRange(client, start: int, end: int, get_json: bool = False) -> Optional[Union[dict, list]]:
        params = [start, end]
        json_data = RPC.make_json(method='sui_getTransactionsInRange', params=params)
        if get_json:
            return json_data

        return RPC.send_request(client=client, json_data=json_data)

    @staticmethod
    def getValidators(client, get_json: bool = False) -> Optional[Union[dict, list]]:
        json_data = RPC.make_json(method='sui_getValidators')
        if get_json:
            return json_data

        return RPC.send_request(client=client, json_data=json_data)

    @staticmethod
    def mergeCoins(client, signer: types.SuiAddress, primary_coin: types.ObjectID,
                   coin_to_merge: types.ObjectID, gas: Optional[types.ObjectID] = None, gas_budget: int = 1_000,
                   get_json: bool = False) -> Optional[Union[dict, list]]:
        params = [signer, primary_coin, coin_to_merge, gas, gas_budget]
        json_data = RPC.make_json(method='sui_mergeCoins', params=params)
        if get_json:
            return json_data

        return RPC.send_request(client=client, json_data=json_data)

    @staticmethod
    def moveCall(client, signer: types.SuiAddress, package_object_id: types.ObjectID, module: str,
                 function: str, type_arguments: Optional[List[types.TypeTag]], arguments: List[types.SuiJsonValue],
                 gas: Optional[types.ObjectID] = None, gas_budget: int = 10_000,
                 get_json: bool = False) -> Optional[Union[dict, list]]:
        params = [signer, package_object_id, module, function, type_arguments, arguments, gas, gas_budget]
        json_data = RPC.make_json(method='sui_moveCall', params=params)
        if get_json:
            return json_data

        return RPC.send_request(client=client, json_data=json_data)

    @staticmethod
    def pay(client, signer: types.SuiAddress, input_coins: List[types.ObjectID],
            recipients: List[types.SuiAddress], amounts: List[int], gas: Optional[types.ObjectID] = None,
            gas_budget: int = 1_000, get_json: bool = False) -> Optional[Union[dict, list]]:
        params = [signer, input_coins, recipients, amounts, gas, gas_budget]
        json_data = RPC.make_json(method='sui_pay', params=params)
        if get_json:
            return json_data

        return RPC.send_request(client=client, json_data=json_data)

    @staticmethod
    def payAllSui(client, signer: types.SuiAddress, input_coins: List[types.ObjectID],
                  recipient: types.SuiAddress, gas_budget: int = 1_000,
                  get_json: bool = False) -> Optional[Union[dict, list]]:
        params = [signer, input_coins, recipient, gas_budget]
        json_data = RPC.make_json(method='sui_payAllSui', params=params)
        if get_json:
            return json_data

        return RPC.send_request(client=client, json_data=json_data)

    @staticmethod
    def paySui(client, signer: types.SuiAddress, input_coins: List[types.ObjectID],
               recipients: List[types.SuiAddress], amounts: List[int], gas_budget: int = 1_000,
               get_json: bool = False) -> Optional[Union[dict, list]]:
        params = [signer, input_coins, recipients, amounts, gas_budget]
        json_data = RPC.make_json(method='sui_paySui', params=params)
        if get_json:
            return json_data

        return RPC.send_request(client=client, json_data=json_data)

    @staticmethod
    def publish(client, sender: types.SuiAddress, compiled_modules: List[types.Base64],
                gas: Optional[types.ObjectID] = None, gas_budget: int = 1_000,
                get_json: bool = False) -> Optional[Union[dict, list]]:
        params = [sender, compiled_modules, gas, gas_budget]
        json_data = RPC.make_json(method='sui_publish', params=params)
        if get_json:
            return json_data

        return RPC.send_request(client=client, json_data=json_data)

    @staticmethod
    def requestAddDelegation(client, signer: types.SuiAddress, coins: List[types.ObjectID], amount: int,
                             validator: types.SuiAddress, gas: Optional[types.ObjectID] = None, gas_budget: int = 1_000,
                             get_json: bool = False) -> Optional[Union[dict, list]]:
        params = [signer, coins, amount, validator, gas, gas_budget]
        json_data = RPC.make_json(method='sui_requestAddDelegation', params=params)
        if get_json:
            return json_data

        return RPC.send_request(client=client, json_data=json_data)

    @staticmethod
    def requestSwitchDelegation(client, signer: types.SuiAddress, delegation: types.ObjectID,
                                staked_sui: types.ObjectID, new_validator_address: types.SuiAddress,
                                gas: Optional[types.ObjectID] = None, gas_budget: int = 1_000,
                                get_json: bool = False) -> Optional[Union[dict, list]]:
        params = [signer, delegation, staked_sui, new_validator_address, gas, gas_budget]
        json_data = RPC.make_json(method='sui_requestSwitchDelegation', params=params)
        if get_json:
            return json_data

        return RPC.send_request(client=client, json_data=json_data)

    @staticmethod
    def requestWithdrawDelegation(client, signer: types.SuiAddress, delegation: types.ObjectID,
                                  staked_sui: types.ObjectID, gas: Optional[types.ObjectID] = None,
                                  gas_budget: int = 1_000, get_json: bool = False) -> Optional[Union[dict, list]]:
        params = [signer, delegation, staked_sui, gas, gas_budget]
        json_data = RPC.make_json(method='sui_requestWithdrawDelegation', params=params)
        if get_json:
            return json_data

        return RPC.send_request(client=client, json_data=json_data)

    @staticmethod
    def splitCoin(client, signer: types.SuiAddress, coin_object_id: types.ObjectID,
                  split_amounts: List[int], gas: Optional[types.ObjectID] = None, gas_budget: int = 1_000,
                  get_json: bool = False) -> Optional[Union[dict, list]]:
        params = [signer, coin_object_id, split_amounts, gas, gas_budget]
        json_data = RPC.make_json(method='sui_splitCoin', params=params)
        if get_json:
            return json_data

        return RPC.send_request(client=client, json_data=json_data)

    @staticmethod
    def splitCoinEqual(client, signer: types.SuiAddress, coin_object_id: types.ObjectID,
                       split_count: int, gas: Optional[types.ObjectID] = None, gas_budget: int = 1_000,
                       get_json: bool = False) -> Optional[Union[dict, list]]:
        params = [signer, coin_object_id, split_count, gas, gas_budget]
        json_data = RPC.make_json(method='sui_splitCoinEqual', params=params)
        if get_json:
            return json_data

        return RPC.send_request(client=client, json_data=json_data)

    @staticmethod
    def subscribeEvent(client, filter: types.EventFilter, get_json: bool = False) -> Optional[Union[dict, list]]:
        params = [filter]
        json_data = RPC.make_json(method='sui_subscribeEvent', params=params)
        if get_json:
            return json_data

        return RPC.send_request(client=client, json_data=json_data)

    @staticmethod
    def tblsSignRandomnessObject(client, object_id: types.ObjectID, commitment_type: str,
                                 get_json: bool = False) -> Optional[Union[dict, list]]:
        params = [object_id, commitment_type]
        json_data = RPC.make_json(method='sui_tblsSignRandomnessObject', params=params)
        if get_json:
            return json_data

        return RPC.send_request(client=client, json_data=json_data)

    @staticmethod
    def transferObject(client, signer: types.SuiAddress, object_id: types.ObjectID, recipient: types.SuiAddress,
                       gas: Optional[types.ObjectID] = None, gas_budget: int = 1_000,
                       get_json: bool = False) -> Optional[Union[dict, list]]:
        params = [signer, object_id, gas, gas_budget, recipient]
        json_data = RPC.make_json(method='sui_transferObject', params=params)
        if get_json:
            return json_data

        return RPC.send_request(client=client, json_data=json_data)

    @staticmethod
    def transferSui(client, signer: types.SuiAddress, sui_object_id: types.ObjectID, gas_budget: int,
                    recipient: types.SuiAddress, amount: int, get_json: bool = False) -> Optional[Union[dict, list]]:
        params = [signer, sui_object_id, gas_budget, recipient, amount]
        json_data = RPC.make_json(method='sui_transferSui', params=params)
        if get_json:
            return json_data

        return RPC.send_request(client=client, json_data=json_data)

    @staticmethod
    def tryGetPastObject(client, object_id: types.ObjectID, version: types.SequenceNumber,
                         get_json: bool = False) -> Optional[Union[dict, list]]:
        params = [object_id, version]
        json_data = RPC.make_json(method='sui_tryGetPastObject', params=params)
        if get_json:
            return json_data

        return RPC.send_request(client=client, json_data=json_data)
