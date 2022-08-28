#!/usr/bin/env python3

import sys
import configparser
from utils import *
from pathlib import Path


def interface(filename:str="wg0", nodename:str="node1"):
    config = configparser.RawConfigParser()
    config.optionxform = str
    config.read("{}.conf".format(filename))
    nodelist = config.sections()[1:]

    # interface generation
    interface = "[Interface]\n" + \
            "Address = " + config[nodename]["Address"][2:-2] + "\n" + \
            "ListenPort = " + config[nodename]["ListenPort"] + "\n" + \
            "PrivateKey = " + config[nodename]["PrivateKey"] + "\n\n" + \
            "PostUp = " + config[nodename]["PostUp"][2:-2] + "\n" + \
            "PostDown = " + config[nodename]["PostDown"][2:-2] + "\n"
    
    with open("{}.conf".format(nodename), "w") as f:
        f.write(interface)
        f.write("\n")

def peer(filename:str="wg0", nodename:str="node1"):
    config = configparser.ConfigParser()
    config.optionxform = str
    config.read("{}.conf".format(filename))
    nodelist = config.sections()[1:]
    nodelist.remove(nodename)

    # peer generation
    for i in range(0, len(nodelist)):
        p_name = nodelist[i]
        peer = "[Peer]\n" + \
                "# Name = " + config[p_name]["Name"] + "\n" + \
                "PublicKey = " + config[p_name]["PublicKey"] + "\n" + \
                "AllowedIPs = " + config[p_name]["AllowedIPs"][2:-2] + "\n"
        if config[p_name]["Endpoint"] != "":
            peer = peer + "Endpoint = " + config[p_name]["Endpoint"] + ":" + config[p_name]["ListenPort"] + "\n"
        with open("{}.conf".format(nodename), "a") as f:
            f.write(peer)
            f.write("\n")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        raise ValueError("Command is needed")
    else:
        interface(filename=sys.argv[1], nodename=sys.argv[2])
        peer(filename=sys.argv[1], nodename=sys.argv[2])
