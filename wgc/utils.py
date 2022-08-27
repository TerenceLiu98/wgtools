import toml
import names
import random
import subprocess as sb
from shutil import which
from serde import serde
from serde.toml import to_toml
from dataclasses import dataclass


"""
dataclass: Node is for the storage all information of the node
"""

@serde
@dataclass
class Node:
    Address: str = None
    IPv4Pool: str = None
    IPv6Pool: str = None



def wgc_genkey():
    wg = which("wg")
    if wg == "None":
        raise ValueError("Please install wireguard before generating the key.")
    else:
        prikey = sb.check_output([wg, "genkey"], text=True).strip()
        pubkey = sb.check_output([wg, "pubkey"], input=prikey, text=True).strip()
        return {"PublicKey": pubkey, "PrivateKey": prikey}

def ipv4Pool():
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

def ipv6Pool():
    """
    from  fd00::/64 to fdff::/64
    """ 
    ipv6 = "{:x}::{}/64".format(random.randint(0xfd00, 0xfdff), random.randint(1, ))
    return ipv6

if __name__ == "__main__":
    pass
