from serde import serde
from serde.toml import from_toml, to_toml
from dataclasses import dataclass, field
from typing import Dict, List, Tuple, Optional

@serde
@dataclass
class Network:
    addr4Pool: str = "192.0.2.0/24"

@serde
@dataclass
class Node:
    Name: str = None
    Address: str = None
    ListenPort: int = None
    PrivateKey: str = ""
    PublicKey: str = ""
    AllowedIPs: str = None
    Endpoint: str = ""
    PreUp: List[str] = field(default_factory=lambda: [])
    PostUp: List[str] = field(default_factory=lambda: [])
    PreDown: List[str] = field(default_factory=lambda: [])
    PostDown: List[str] = field(default_factory=lambda: [])
    PersistentKeepalive: int = 25

