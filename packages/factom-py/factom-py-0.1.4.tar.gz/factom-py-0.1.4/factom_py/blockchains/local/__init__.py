from .constants import LOCAL_NETWORK_ID

from factom_py.blockchains import Blockchain


class LocalBlockchain(Blockchain):
    network_id = LOCAL_NETWORK_ID
