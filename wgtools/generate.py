import sys
import configparser
from utils import *
from pathlib import Path
from copy import deepcopy


def interface(filename:str="wg0", nodename:str="node1"):
    config = configparser.RawConfigParser()
    config.optionxform = str
    config.read(f"{filename}/{filename}.conf")
    nodelist = config.sections()[1:]
    nodelist.remove(nodename)

    bridge_statement = ""
    for i in range(0, len(nodelist)):
        p_name = nodelist[i]
        wgAddress = config[p_name]["wgAddress"]
        bridge_statement = bridge_statement + f"PostUp = bridge fdb append to 00:00:00:00:00:00 dst {wgAddress[:-3]} dev v%i" + "\n" \

    # interface generation
    interface = "[Interface]\n" + \
            "Address = " + config[nodename]["wgAddress"] + "\n" + \
            "ListenPort = " + config[nodename]["ListenPort"] + "\n" + \
            "PrivateKey = " + config[nodename]["PrivateKey"] + "\n\n" + \
            "# PostUp = " + config[nodename]["PostUp"] + "\n" + \
            "# PostDown = " + config[nodename]["PostDown"] + "\n" + \
            "Table = off" + "\n" + \
            "PostUp = ip link add v%i type vxlan id {} dstport 4789 ttl 1 dev %i".format(config["Network"]["vxlan_id"]) + "\n" + \
            bridge_statement + \
            "PostUp = ip address add {} dev v%i".format(config[nodename]["v4Address"]) + "\n" + \
            "PostUp = ip address add {} dev v%i".format(config[nodename]["v6Address"]) + "\n" + \
            "PostUp = ip link set v%i up" + "\n" + \
            "PreDown = ip link set v%i down" + "\n" + \
            "PreDown = ip link delete v%i" + "\n"

    
    with open(f"{filename}/{nodename}.conf", "w") as f:
        f.write(interface)
        f.write("\n")

def peer(filename:str="wg0", nodename:str="node1"):
    if nodename != None:
        config = configparser.ConfigParser()
        config.optionxform = str
        config.read(f"{filename}/{filename}.conf")
        nodelist = config.sections()[1:]
        nodelist.remove(nodename)

        # peer generation
        interface(filename=filename, nodename=nodename)
        for i in range(0, len(nodelist)):
            p_name = nodelist[i]
            peer = "[Peer]\n" + \
                    "# Name = " + config[p_name]["Name"] + "\n" + \
                    "PublicKey = " + config[p_name]["PublicKey"] + "\n" + \
                    "AllowedIPs = " + config[p_name]["AllowedIPs"] + "\n" + \
                    "PersistentKeepalive = " + config[p_name]["PersistentKeepalive"] + "\n"
            if config[p_name]["Endpoint"] != "":
                peer = peer + "Endpoint = " + config[p_name]["Endpoint"] + ":" + config[p_name]["ListenPort"] + "\n"
            with open(f"{filename}/{nodename}.conf", "a") as f:
                f.write(peer)
                f.write("\n")
    else:
        config = configparser.ConfigParser()
        config.optionxform = str
        config.read(f"{filename}/{filename}.conf")
        nodelist = config.sections()[1:]

        # peer generation
        for i in range(0, len(nodelist)):
            tmp_nodelist, nodename = deepcopy(nodelist), nodelist[i]
            interface(filename=filename, nodename=nodename)
            tmp_nodelist.remove(nodelist[i])
            for j in range(0, len(tmp_nodelist)):
                p_name = tmp_nodelist[j]
                peer = "[Peer]\n" + \
                        "# Name = " + config[p_name]["Name"] + "\n" + \
                        "PublicKey = " + config[p_name]["PublicKey"] + "\n" + \
                        "AllowedIPs = " + config[p_name]["AllowedIPs"] + "\n" + \
                        "PersistentKeepalive = " + config[p_name]["PersistentKeepalive"] + "\n"
                if config[p_name]["Endpoint"] != "":
                    peer = peer + "Endpoint = " + config[p_name]["Endpoint"] + ":" + config[p_name]["ListenPort"] + "\n"
                with open(f"{filename}/{nodename}.conf", "a") as f:
                    f.write(peer)
                    f.write("\n")

if __name__ == "__main__":
    #interface(filename=sys.argv[1], nodename=sys.argv[2])
    try:
        peer(filename=sys.argv[1], nodename=sys.argv[2])
    except:
        peer(filename=sys.argv[1], nodename=None)
