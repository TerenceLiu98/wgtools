import sys
import configparser
from utils import *
from pathlib import Path
from copy import deepcopy

def get_port(data, target_nodename):
    for item in data:
        if item['nodename'] == target_nodename:
            return str(item['port'])
    return None

def interface(filename:str="wg0", nodename:str="node1", udp2raw:bool=False):
    config = configparser.RawConfigParser()
    config.optionxform = str
    config.read(f"{filename}/{filename}.conf")
    nodelist = config.sections()[1:]
    nodelist.remove(nodename)
    listen_port = []
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
    
    if udp2raw and config[nodename]["Endpoint"] != "":
        interface = interface + "PostUp = udp2raw -s -l0.0.0.0:{} -r127.0.0.1:{} -k 'passwd' --raw-mode faketcp -a >/var/log/udp2raw.log 2>&1 &".format(config[nodename]["ListenPort"], config[nodename]["ListenPort"]) + "\n" + \
                                "PostDown = killall -TERM udp2raw" + "\n"
    elif udp2raw and config[nodename]["Endpoint"] == "":
        for i in range(0, len(nodelist)):
            p_name = nodelist[i]
            if config[p_name]["Endpoint"] != "":
                port = random.randint(51820, 51900)
                interface = interface + "PostUp = udp2raw -c -l0.0.0.0:{} -r{}:{} -k 'passwd' --raw-mode faketcp -a >/var/log/udp2raw-{}.log 2>&1 &".format(port,
                                                                                                                                                            config[p_name]["Endpoint"], 
                                                                                                                                                            config[p_name]["ListenPort"], i) + "\n"
                listen_port.append({"nodename": p_name, "port": port})
            else:
                pass
        interface = interface + "PostDown = killall -TERM udp2raw" + "\n"
    else:
        pass
    
    with open(f"{filename}/{nodename}.conf", "w") as f:
        f.write(interface)
        f.write("\n")
    
    return listen_port

def peer(filename:str="wg0", nodename:str="node1", udp2raw:bool=False):
    if nodename != None:
        config = configparser.ConfigParser()
        config.optionxform = str
        config.read(f"{filename}/{filename}.conf")
        nodelist = config.sections()[1:]
        nodelist.remove(nodename)

        # peer generation
        listen_port = interface(filename=filename, nodename=nodename, udp2raw=udp2raw)
        for i in range(0, len(nodelist)):
            p_name = nodelist[i]
            peer = "[Peer]\n" + \
                    "# Name = " + config[p_name]["Name"] + "\n" + \
                    "PublicKey = " + config[p_name]["PublicKey"] + "\n" + \
                    "AllowedIPs = " + config[p_name]["AllowedIPs"] + "\n" + \
                    "PersistentKeepalive = " + config[p_name]["PersistentKeepalive"] + "\n"
            if config[nodename]["Endpoint"] == "" and config[p_name]["Endpoint"] != "":
                peer = peer + "Endpoint = " + "127.0.0.1" + ":" + get_port(listen_port, p_name) + "\n"
            elif config[nodename]["Endpoint"] != "" and config[p_name]["Endpoint"] != "":
                peer = peer + "Endpoint = " + config[p_name]["Endpoint"] + ":" + config[p_name]["ListenPort"] + "\n"
            else:
                pass
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
            listen_port = interface(filename=filename, nodename=nodename, udp2raw=udp2raw)
            tmp_nodelist.remove(nodelist[i])
            for j in range(0, len(tmp_nodelist)):
                p_name = tmp_nodelist[j]
                peer = "[Peer]\n" + \
                        "# Name = " + config[p_name]["Name"] + "\n" + \
                        "PublicKey = " + config[p_name]["PublicKey"] + "\n" + \
                        "AllowedIPs = " + config[p_name]["AllowedIPs"] + "\n" + \
                        "PersistentKeepalive = " + config[p_name]["PersistentKeepalive"] + "\n"
                if config[nodename]["Endpoint"] == "" and config[p_name]["Endpoint"] != "":
                    peer = peer + "Endpoint = " + "127.0.0.1" + ":" + get_port(listen_port, p_name) + "\n"
                elif config[nodename]["Endpoint"] != "" and config[p_name]["Endpoint"] != "":
                    peer = peer + "Endpoint = " + config[p_name]["Endpoint"] + ":" + config[p_name]["ListenPort"] + "\n"
                else:
                    pass
                with open(f"{filename}/{nodename}.conf", "a") as f:
                    f.write(peer)
                    f.write("\n")

if __name__ == "__main__":
    #interface(filename=sys.argv[1], nodename=sys.argv[2])
    try:
        try:
            peer(filename=sys.argv[1], nodename=sys.argv[2], udp2raw=sys.argv[3])
        except:
            peer(filename=sys.argv[1], nodename=sys.argv[2])
    except:
        try:
            peer(filename=sys.argv[1], nodename=None, udp2raw=sys.argv[2])
        except:
            peer(filename=sys.argv[1], nodename=None)