from typing import Optional

import requests


class ClientException(Exception):
    pass


class InvalidProxy(ClientException):
    pass


class RPCException(ClientException):
    def __init__(self, response: Optional[requests.Response] = None, code: Optional[int] = None,
                 message: Optional[str] = None) -> None:
        self.response = response
        self.code = code
        self.message = message

    def __str__(self):
        if self.code:
            return f'{self.code}, {self.message}'

        return f'{self.response.status_code}'


class NFTException(Exception):
    pass


class TransactionException(Exception):
    pass


class InsufficientGas(TransactionException):
    pass


class NoSuchToken(TransactionException):
    pass


class InsufficientBalance(TransactionException):
    pass


class WalletException(Exception):
    pass


class NoObjects(WalletException):
    pass


class FaucetException(WalletException):
    pass
