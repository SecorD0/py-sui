class ClientException(Exception):
    pass


class InvalidProxy(ClientException):
    pass


class RPCException(ClientException):
    pass


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
