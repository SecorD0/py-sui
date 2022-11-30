import os
from typing import Optional

from dotenv import load_dotenv

from py_sui.client import Client
from py_sui.models import Nft


class Test:
    @staticmethod
    def print_balance(balance):
        print(f'''Balance instance:
{balance}

Coin:
{balance.coin}''')

        if balance.tokens:
            print(f'\nTokens ({len(balance.tokens)}):')
            for obj_id, value in balance.tokens.items():
                print(obj_id, value)

        if balance.nfts:
            print(f'\nNFTs ({len(balance.nfts)}):')
            for obj_id, value in balance.nfts.items():
                print(obj_id, value)

        if balance.misc:
            print(f'\nMiscellaneous ({len(balance.misc)}):')
            for obj_id, value in balance.misc.items():
                print(obj_id, value)

    @staticmethod
    def balance(address: str):
        """Show balance."""
        client = Client('')

        balance = client.wallet.balance(address)

        Test.print_balance(balance)
        print('----------------------------------------------------------------------------')

    @staticmethod
    def generate_wallet():
        client = Client()
        print(client.account)

        print('----------------------------------------------------------------------------')

    @staticmethod
    def request_sui_coins():
        client = Client(mnemonic, proxy)
        print(client.account)

        print(client.wallet.request_coins_from_faucet())
        Test.my_balance()

        print('----------------------------------------------------------------------------')

    @staticmethod
    def my_balance():
        client = Client(mnemonic, proxy)
        print(client.account)

        balance = client.wallet.balance()
        Test.print_balance(balance)
        print('----------------------------------------------------------------------------')

    @staticmethod
    def mint_example_nft():
        client = Client(mnemonic, proxy)
        print(client.account)

        balance = client.wallet.balance()
        for obj_id, value in balance.nfts.items():
            print(obj_id, value)

        print()

        print(client.nfts.mint_example_nft())
        balance = client.wallet.balance()
        for obj_id, value in balance.nfts.items():
            print(obj_id, value)

        print('----------------------------------------------------------------------------')

    @staticmethod
    def mint_wizard_nft():
        client = Client(mnemonic, proxy)
        print(client.account)

        balance = client.wallet.balance()
        for obj_id, value in balance.nfts.items():
            print(obj_id, value)

        print()

        nft = Nft(arguments=["Wizard Land", "Expanding The Magic Land",
                             "https://gateway.pinata.cloud/ipfs/QmYfw8RbtdjPAF3LrC6S3wGVwWgn6QKq4LGS4HFS55adU2?w=800&h=450&c=crop"])
        client.nfts.mint(nft=nft)
        balance = client.wallet.balance()
        for obj_id, value in balance.nfts.items():
            print(obj_id, value)

        print('----------------------------------------------------------------------------')

    @staticmethod
    def mint_bluemove_nft():
        client = Client(mnemonic, proxy)
        print(client.account)

        balance = client.wallet.balance()
        for obj_id, value in balance.nfts.items():
            print(obj_id, value)

        print()
        arguments = ['0x081e876200a657e173397f722aba3b6628c6d270', 1]
        client.transactions.move_call(package_object_id='0x3c2468cdc0288983f099a52fc6f5b43e4ed0c959',
                                      module='bluemove_launchpad', function='mint_with_quantity', type_arguments=[],
                                      arguments=arguments, gas_budget=50_000)

        balance = client.wallet.balance()
        for obj_id, value in balance.nfts.items():
            print(obj_id, value)

        print('----------------------------------------------------------------------------')

    @staticmethod
    def send_coin():
        client = Client(mnemonic, proxy)
        print(client.account)

        balance = client.wallet.balance()
        print(balance.coin)

        print(client.transactions.send_coin(client.account.address, 100_000))

        balance = client.wallet.balance()
        print(balance.coin)

        print('----------------------------------------------------------------------------')

    @staticmethod
    def send_token(token: str):
        client = Client(mnemonic, proxy)
        print(client.account)

        balance = client.wallet.balance()
        print(balance.tokens[token])

        print(client.transactions.send_token(balance.tokens[token], client.account.address, 10_000))

        balance = client.wallet.balance()
        print(balance.coin)

        print('----------------------------------------------------------------------------')

    @staticmethod
    def send_nft(nft: str):
        client = Client(mnemonic, proxy)
        print(client.account)

        balance = client.wallet.balance()
        for obj_id, value in balance.nfts.items():
            print(obj_id, value)

        print(client.transactions.send_nft(balance.nfts[nft], client.account.address))

        balance = client.wallet.balance()
        for obj_id, value in balance.nfts.items():
            print(obj_id, value)

        print('----------------------------------------------------------------------------')

    @staticmethod
    def merge_coin():
        client = Client(mnemonic, proxy)
        print(client.account)

        balance = client.wallet.balance()
        print(balance.coin)

        print(client.transactions.merge_coin(balance.coin))

        balance = client.wallet.balance()
        print(balance.coin)

        print('----------------------------------------------------------------------------')

    @staticmethod
    def merge_token(token: str):
        client = Client(mnemonic, proxy)
        print(client.account)

        balance = client.wallet.balance()
        print(balance.tokens[token])

        print(client.transactions.merge_coin(balance.tokens[token]))

        balance = client.wallet.balance()
        print(balance.tokens[token])

        print('----------------------------------------------------------------------------')

    @staticmethod
    def history(address: Optional[str] = None):
        if address:
            client = Client('')

        else:
            client = Client(mnemonic, proxy)
            print(client.account)

        history = client.transactions.history(address)
        print(f'Incoming ({len(history.incoming)}):')
        for tx in history.incoming:
            print(tx)

        print()

        print(f'Outgoing ({len(history.outgoing)}):')
        for tx in history.outgoing:
            print(tx)

        print('----------------------------------------------------------------------------')


if __name__ == '__main__':
    load_dotenv()
    mnemonic = str(os.getenv('MNEMONIC'))
    proxy = str(os.getenv('PROXY'))
    test = Test()
    test.balance('0xc4173a804406a365e69dfb297d4eaaf002546ebd')
    test.generate_wallet()
    test.request_sui_coins()
    test.my_balance()
    test.mint_example_nft()
    test.mint_wizard_nft()
    test.mint_bluemove_nft()
    test.send_coin()
    test.send_token('usdt')
    test.send_nft('0x1c47664b9b12fca8ede96726b6d90c854ae512a7')
    test.merge_coin()
    test.merge_token('usdt')
    test.history()
    test.history('0x0f2df809112256ec9068c2663bc4901c8a1b3ce7')
