from serde import serde
from serde.toml import from_toml, to_toml
from dataclasses import dataclass

@serde
@dataclass
class Network:
    addr4Pool: str = "192.0.2.0/24"
    addr6Pool: str = "2001:DB8::/32"

@serde
@dataclass
class Node:
    Name: str = None
    Address: str = None
    ListenPort: int = 51820
    PrivateKey: str = None
    PublicKey: str = None
    AllowedIPs: str = None
    Endpoint: str = None
    PreUp: dict = None
    PostUp: dict = None
    PreDown: dict = None
    PostDown: dict = None
    PersistentKeepalive: int = 25

