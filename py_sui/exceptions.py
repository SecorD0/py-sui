from typing import Optional

import requests


class ClientException(Exception):
    pass


class InvalidProxy(ClientException):
    pass


class RPCException(ClientException):
    def __init__(self, response: Optional[requests.Response]):
        self.response = response


class NFTException(Exception):
    pass


class TransactionException(Exception):
    pass


class InsufficientGas(TransactionException):
    pass


class NoSuchToken(TransactionException):
    pass


class WalletException(Exception):
    pass


class FaucetException(WalletException):
    pass
