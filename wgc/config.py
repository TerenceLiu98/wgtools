import toml
import ipaddress

@dataclass
class Interface:
    Address: str = None
    ListentPort: str = None
    PrivateKey: str = None

@dataclass
class Peer:
    PublicKey: str = None
    PresharedKey: str = None
    Endpoint: str = None
    AllowedIPs: str = None
