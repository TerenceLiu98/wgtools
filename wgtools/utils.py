import base64
import random
from pathlib import Path
from dataclasses import dataclass
from configparser import ConfigParser, RawConfigParser
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric.x25519 import X25519PrivateKey

@dataclass
class Network:
    v4addr: str = ""
    v6addr: str = ""

@dataclass
class Node:
    Address: str = ""
    ListenPort: int = 51820
    PrivateKey: str = ""
    PublicKey: str = ""
    PostUp: str = "iptables -A FORWARD -i %i -j ACCEPT; iptables -A FORWARD -o %i -j ACCEPT; iptables -t nat -A POSTROUTING -o eth0 -j MASQUERADE"
    PostDown: str = "iptables -D FORWARD -i %i -j ACCEPT; iptables -D FORWARD -o %i -j ACCEPT; iptables -t nat -D POSTROUTING -o eth0 -j MASQUERADE"
    Endpoint: str = ""
    AllowedIPs: str = ""

def genkey():
    privkey = base64.b64encode(X25519PrivateKey.generate().private_bytes(
        encoding=serialization.Encoding.Raw,
        format=serialization.PrivateFormat.Raw,
        encryption_algorithm=serialization.NoEncryption()
    )).decode()
    pubkey = base64.b64encode(X25519PrivateKey.from_private_bytes(
                base64.b64decode(privkey.encode())
            ).public_key().public_bytes(
                encoding=serialization.Encoding.Raw,
                format=serialization.PublicFormat.Raw,
            )
        ).decode()
    return privkey, pubkey


def v4Pool():
    """
    A: 10.0.0.0 to 10.255.255.255
    B: 172.16.0.0 to 172.31.255.255
    C: 192.168.0.0 to 192.168.255.255
    """
    intranet_dict = ["A", "B", "C"]
    intranet = intranet_dict[int("{}".format(random.randint(0, 2)))]
    if intranet == "A":
        ipv4 = "10.{}.{}.0/24".format(random.randint(0, 255), random.randint(0, 255))
    if intranet == "B":
        ipv4 = "172.{}.{}.0/24".format(random.randint(16, 31), random.randint(0, 255))
    if intranet == "C":
        ipv4 = "192.168.{}.0/24".format(random.randint(0, 255))
    return ipv4

def v6Pool():
    """
    from  fd00::/64 to fdff::/64
    """ 
    ipv6 = "{:x}::{}/64".format(random.randint(0xfd00, 0xfdff), random.randint(1, 254))
    return ipv6
