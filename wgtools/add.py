#!/usr/bin/python3

from utils import *

def network(filename="wg0"):
    """Add a new network interface"""
    if Path(f"{filename}.conf").exists():
        return ValueError("File already exists")
    else:
        network = Network(v4addr=v4Pool(), v6addr=v6Pool())
        config = ConfigParser()
        config["Network"] = network.__dict__
        with open(f"{filename}.conf", "w") as f:
            config.write(f)
            f.write("\n")


def node(filename="wg0", nodename="node1"):
    """Add a new node to the network"""
    if Path(f"{filename}.conf").exists():
        config = RawConfigParser()
        config.optionxform = str
        config.read(f"{filename}.conf")
        if nodename in config.sections():
            return ValueError("Node already exists")
        else:
            node = Node()
            node.Name = nodename
            node.Address = random_v4_addr(network=config["Network"]["v4addr"]) + "/32" + "," + \
                            random_v6_addr(network=config["Network"]["v6addr"]) + "/128"
            node.PrivateKey, node.PublicKey = genkey()
            node.AllowedIPs = node.Address
            config[nodename] = node.__dict__
            with open(f"{filename}.conf", "w") as f:
                config.write(f)
                f.write("\n")
    else:
        return ValueError("Network does not exist")



        

