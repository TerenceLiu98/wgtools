#!/usr/bin/env python3

import sys
import configparser
from utils import *
from pathlib import Path


def network(filename:str="wg0"):

    if Path("{}.conf".format(filename)).is_file():
        raise OSError("This configuration exists in local directory")
    else:
        network = Network(addr4Pool=ipv4Pool())
        network_info = "[Network]\n" + to_toml(network).replace('"', "")
        with open("{}.conf".format(filename), "w") as f:
            f.write(network_info)
        return 0

def node(filename:str="wg0", nodename:str="node1"):
    config = configparser.ConfigParser()
    config.optionxform = str
    config.read("{}.conf".format(filename))
    node = Node()
    node.Name = nodename
    node.Address.append("".join(config["Network"]["addr4Pool"][:-4] + str(random.randint(1, 255)) + "/24"))
    node.ListenPort = random.randint(32768, 60999)
    node.PrivateKey, node.PublicKey = wgc_genkey()
    node.AllowedIPs.append("".join(node.Address[0][:-3] + "/32"))
    node_info = "\n[{}]\n".format(node.Name) + to_toml(node).replace('"', "")
    with open("{}.conf".format(filename), "a") as f:
        f.write(node_info)
    return 0

if __name__ == "__main__":
    if len(sys.argv) < 2:
        raise ValueError("Command is needed")
    else:
        if sys.argv[1] == "network":
            network(filename=sys.argv[2])
        else:
            node(filename=sys.argv[1], nodename=sys.argv[2])
