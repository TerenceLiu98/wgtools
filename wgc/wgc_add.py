#!/usr/bin/env python3

import sys
import configparser
from utils import *
from config import *
from pathlib import Path


def network(filename:str="wg0"):

    if Path("{}".format(filename)).is_file():
        raise OSError("This configuration exists in local directory")
    else:
        network = Network()
        network_info = "[Network]\n" + to_toml(network).replace('"', "")
        with open("{}.conf".format(filename), "w") as f:
            f.write(network_info)
        return 0

def node(filename:str="wg0"):
    config = configparser.ConfigParser()
    config.read("{}.conf".format(filename))
    node = Node()
    node.Name = names.get_first_name()
    node.Address = config["Network"]["addr4Pool"][:-4] + str(random.randint(1, 255)) + "/24"
    node.ListenPort = random.randint(32768, 60999)
    node.Privatekey, node.PublicKey = wgc_genkey()
    AllowedIPs = node.Address[:-2] + "/32"
    node_info = "\n[Node.{}]\n".format(node.Name) + to_toml(node).replace('"', "")
    with open("{}.conf".format(filename), "a") as f:
        f.write(node_info)
    return 0
