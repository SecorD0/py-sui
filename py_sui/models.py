from dataclasses import dataclass
from typing import Optional, List, Dict


class Types:
    Base64 = str
    EventFilter = str
    EventID = str
    EventQuery = dict
    ExecuteTransactionRequestType = str
    ObjectID = str
    RPCTransactionRequestParams = dict
    SequenceNumber = int
    SignatureScheme = str
    SuiAddress = str
    SuiJsonValue = dict or list
    TransactionDigest = str
    TransactionQuery = dict
    TxBytes = bytes
    TxHash = bytes
    TypeTag = str


class SignatureScheme:
    ED25519 = 'ED25519'
    Secp256k1 = 'Secp256k1'


class ExecuteType:
    ImmediateReturn = 'ImmediateReturn'
    WaitForTxCert = 'WaitForTxCert'
    WaitForEffectsCert = 'WaitForEffectsCert'
    WaitForLocalExecution = 'WaitForLocalExecution'


@dataclass
class Network:
    rpc: str
    explorer: Optional[str] = None
    faucet: Optional[str] = None


class Networks:
    Devnet = Network(rpc='https://fullnode.devnet.sui.io/', explorer='https://explorer.sui.io/{}?network=devnet',
                     faucet='https://faucet.devnet.sui.io/gas')
    Staging = Network(rpc='https://fullnode.staging.sui.io/', faucet='https://faucet.staging.sui.io/gas')
    Testnet = Network(rpc='https://fullnode.testnet.sui.io/', explorer='https://explorer.sui.io/{}?network=testnet',
                      faucet='https://faucet.testnet.sui.io/gas')


@dataclass
class StringAndBytes:
    str_: str
    bytes_: bytes


@dataclass
class WalletInfo:
    mnemonic: str
    private_key: StringAndBytes
    public_key: StringAndBytes
    address: str


@dataclass
class Tx:
    digest: str
    status: str
    sender: str
    recipients: Optional[List[str]]
    transactions: List[dict]
    raw_dict: dict


@dataclass
class History:
    incoming: List[Tx]
    outgoing: List[Tx]


@dataclass
class ObjectType:
    raw_type: str
    type: Optional[str] = None
    package_id: Optional[str] = None
    name: Optional[str] = None
    symbol: Optional[str] = None


@dataclass
class ObjectID:
    id: str
    amount: int


@dataclass
class Coin:
    name: str
    symbol: str
    package_id: str
    balance: float
    object_ids: List[ObjectID]


@dataclass
class Nft:
    name: str
    description: str
    image_url: str
    object_id: Optional[str] = None


@dataclass
class Balance:
    coin: Optional[Coin] = None
    tokens: Optional[Dict[str, Coin]] = None
    nfts: Optional[Dict[str, Nft]] = None
    misc: Optional[Dict[str, dict]] = None
