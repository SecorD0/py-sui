import base64
import hashlib
from typing import Optional

import bip_utils
import nacl
import requests
from bs4 import BeautifulSoup as BS
from fake_useragent import UserAgent
from pretty_utils.type_functions.strings import text_between

from py_sui import exceptions
from py_sui.models import Network, Networks, WalletInfo, SignatureScheme, ExecuteType, StringAndBytes
from py_sui.nfts import NFT
from py_sui.rpc_methods import RPC
from py_sui.transactions import Transaction
from py_sui.wallet import Wallet


class Client:
    def __init__(self, mnemonic: Optional[str] = None, proxy: Optional[str] = None, network: Network = Networks.Testnet,
                 check_proxy: bool = True, derivation_path: str = "m/44'/784'/0'/0'/0'") -> None:
        self.network = network
        self.derivation_path = derivation_path

        self.proxy = proxy
        self.session = requests.Session()
        self.session.headers.update({
            'authority': self.network.rpc.replace('https:', '').replace('/', ''),
            'accept': '*/*',
            'accept-language': 'en-US,en;q=0.9',
            'origin': 'chrome-extension://opcgpfmipidbgpenhmajoajpbobppdil',
            'user-agent': UserAgent().chrome,
            'Content-type': 'application/json'
        })

        if self.proxy:
            try:
                if 'http' not in self.proxy:
                    self.proxy = f'http://{self.proxy}'

                proxies = {'http': self.proxy, 'https': self.proxy}
                self.session.proxies.update(proxies)
                if check_proxy:
                    response = self.session.get('https://whoer.net/')
                    if '@' in self.proxy:
                        proxy = text_between(self.proxy, '@', ':')
                    else:
                        proxy = text_between(self.proxy, end=':')

                    if proxy not in response.text:
                        soup = BS(response.text, 'html.parser')
                        your_ip = soup.find('strong', class_='your-ip').get_text(strip=True)
                        raise exceptions.InvalidProxy(f"Proxy doesn't work! Your IP is {your_ip}")

            except Exception as e:
                raise exceptions.InvalidProxy(str(e))

        self.account: Optional[WalletInfo] = None
        if mnemonic or mnemonic is None:
            if mnemonic is None:
                mnemonic = bip_utils.Bip39MnemonicGenerator().FromWordsNumber(
                    bip_utils.Bip39WordsNum.WORDS_NUM_12).ToStr()

            bip39_seed = bip_utils.Bip39SeedGenerator(mnemonic).Generate()
            bip32_ctx = bip_utils.Bip32Slip10Ed25519.FromSeed(bip39_seed)
            bip32_der_ctx = bip32_ctx.DerivePath(self.derivation_path)

            private_key = bip32_der_ctx.PrivateKey().Raw()
            private_key = StringAndBytes(str_="0x" + str(private_key), bytes_=private_key.ToBytes())
            public_key = bip32_der_ctx.PublicKey().RawCompressed()
            public_key = StringAndBytes(str_="0x" + str(public_key), bytes_=public_key.ToBytes())
            address = "0x" + hashlib.sha3_256(public_key.bytes_).digest().hex()[:40]

            self.account = WalletInfo(mnemonic=mnemonic, private_key=private_key, public_key=public_key,
                                      address=address)

        self.nfts = NFT(self)
        self.transactions = Transaction(self)
        self.wallet = Wallet(self)

    def sign_data(self, data: bytes) -> Optional[bytes]:
        return nacl.signing.SigningKey(self.account.private_key.bytes_).sign(data)[:64]

    def sign_and_execute_transaction(self, tx_bytes: bytes) -> Optional[dict]:
        signature_bytes = self.sign_data(tx_bytes)

        tx_bytes = base64.b64encode(tx_bytes).decode()
        sig_scheme = SignatureScheme.ED25519
        signature = base64.b64encode(signature_bytes).decode()
        pub_key = base64.b64encode(self.account.public_key.bytes_[1:]).decode()
        request_type = ExecuteType.WaitForLocalExecution

        return RPC.executeTransaction(client=self, tx_bytes=tx_bytes, sig_scheme=sig_scheme, signature=signature,
                                      pub_key=pub_key, request_type=request_type)
