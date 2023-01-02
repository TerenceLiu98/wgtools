#!/usr/bin/python3
import sys
import pathlib
from utils import *

def network(filename="wg0"):
    """Add a new network interface"""
    if Path(f"{filename}.conf").exists():
        return ValueError("File already exists")
    else:
        network = Network(v4addr=v4Pool(), v6addr=v6Pool(), vxlan_id=random.randint(10000, 50000),wg_addr=v4Pool(intranet="D"))
        config = ConfigParser()
        config["Network"] = network.__dict__
        with open(f"{filename}/{filename}.conf", "w") as f:
            config.write(f)
            f.write("\n")

def node(filename="wg0", nodename="node71"):
    """Add a new node to the network"""
    if Path(f"{filename}/{filename}.conf").exists():
        config = RawConfigParser()
        config.optionxform = str
        config.read(f"{filename}/{filename}.conf")
        if nodename in config.sections():
            return ValueError("Node already exists")
        else:
            node = Node()
            node.Name = nodename
            node.v4Address = random_v4_addr(network=config["Network"]["v4addr"]) + "/24"
            node.v6Address = random_v6_addr(network=config["Network"]["v6addr"]) + "/64"
            node.wgAddress = random_v4_addr(network=config["Network"]["wg_addr"]) + "/24"
            node.PrivateKey, node.PublicKey = genkey()
            node.AllowedIPs = node.wgAddress[:-2] + "32"
            config[nodename] = node.__dict__
            with open(f"{filename}/{filename}.conf", "w") as f:
                config.write(f)
                f.write("\n")
    else:
        return ValueError("Network does not exist")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        raise ValueError("Command is needed")
    else:
        if sys.argv[1] == "network":
            pathlib.Path(f'{sys.argv[2]}').mkdir(parents=True, exist_ok=True)
            network(filename=sys.argv[2])

        else:
            node(filename=sys.argv[2], nodename=sys.argv[3])



        

