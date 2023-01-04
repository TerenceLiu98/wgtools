import sys
import json
import configparser
from utils import *
from pathlib import Path


def interface(filename:str="wg0", nodename:str="node1"):
    with open(f"{filename}/{filename}.json", "r+") as f:
        config = json.load(f)
        f.close()
    peerlist = list(config["nodelist"].keys())
    peerlist.remove(nodename)

    bridge_statement = ""
    for i in range(0, len(peerlist)):
        peer_name = peerlist[i]
        wgAddress = config["nodelist"][peer_name]["wgAddress"]
        bridge_statement = bridge_statement + f"PostUp = bridge fdb append to 00:00:00:00:00:00 dst {wgAddress[:-3]} dev v%i" + "\n" \

    # interface generation
    interface = "[Interface]\n" + \
            "Address = " + str(config["nodelist"][nodename]["wgAddress"]) + "\n" + \
            "ListenPort = " + str(config["nodelist"][nodename]["ListenPort"]) + "\n" + \
            "PrivateKey = " + str(config["nodelist"][nodename]["PrivateKey"]) + "\n\n" + \
            "# PostUp = " + str(config["nodelist"][nodename]["PostUp"]) + "\n" + \
            "# PostDown = " + str(config["nodelist"][nodename]["PostDown"]) + "\n" + \
            "Table = off" + "\n" + \
            "PostUp = ip link add v%i type vxlan id {} dstport 4789 ttl 1 dev %i".format(config["vxlan_id"]) + "\n" + \
            bridge_statement + \
            "PostUp = ip address add {} dev v%i".format(config["nodelist"][nodename]["v4Address"]) + "\n" + \
            "PostUp = ip address add {} dev v%i".format(config["nodelist"][nodename]["v6Address"]) + "\n" + \
            "PostUp = ip link set v%i up" + "\n" + \
            "PreDown = ip link set v%i down" + "\n" + \
            "PreDown = ip link delete v%i" + "\n"

    
    with open(f"{filename}/{nodename}.conf", "w") as f:
        f.write(interface)
        f.write("\n")
        f.close()

def peer(filename:str="wg0", nodename:str="node1"):
    with open(f"{filename}/{filename}.json", "r+") as f:
        config = json.load(f)
        f.close()
    peerlist = list(config["nodelist"].keys())
    peerlist.remove(nodename)

    # peer generation
    for i in range(0, len(peerlist)):
        peer_name = peerlist[i]
        peer = "[Peer]\n" + \
                "# Name = " + str(config["nodelist"][peer_name]["Name"]) + "\n" + \
                "PublicKey = " + str(config["nodelist"][peer_name]["PublicKey"]) + "\n" + \
                "AllowedIPs = " + str(config["nodelist"][peer_name]["AllowedIPs"]) + "\n" + \
                "PersistentKeepalive = " + str(config["nodelist"][peer_name]["PersistentKeepalive"]) + "\n"
        if config["nodelist"][peer_name]["Endpoint"] != "":
            peer = peer + "Endpoint = " + config["nodelist"][peer_name]["Endpoint"] + ":" + str(config["nodelist"][peer_name]["ListenPort"]) + "\n"
        with open(f"{filename}/{nodename}.conf", "a") as f:
            f.write(peer)
            f.write("\n")

if __name__ == "__main__":
    interface(filename=sys.argv[1], nodename=sys.argv[2])
    peer(filename=sys.argv[1], nodename=sys.argv[2])
