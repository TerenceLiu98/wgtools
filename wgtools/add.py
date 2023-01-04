#!/usr/bin/python3
import sys
import uuid
import json
import pathlib
from utils import *

def network(filename="wg0"):
    """Add a new network interface"""
    if Path(f"{filename}.conf").exists():
        return ValueError("File already exists")
    else:
        network = Network(name=filename, v4addr=v4Pool(), v6addr=v6Pool(), 
            vxlan_id=random.randint(10000, 50000), wg_addr=v4Pool(intranet="D"), nodelist={})
        network = network.__dict__
        with open(f"{filename}/{filename}.json", "w") as f:
            json.dump(network, f)
            f.close()

def node(filename="wg0", nodename="node71"):
    """Add a new node to the network"""
    if Path(f"{filename}/{filename}.json").exists():
        with open(f"{filename}/{filename}.json", "r+") as f:
            file = json.load(f)
            f.close()
        if nodename in list(file["nodelist"].keys()):
            return ValueError("Node already exists")
        else:
            node = Nodeinfo()
            node.Name = nodename
            node.nid = str(uuid.uuid3(uuid.NAMESPACE_URL, f"https://{nodename}.{filename}.local"))
            node.v4Address = random_v4_addr(network=file["v4addr"]) + "/24"
            node.v6Address = random_v6_addr(network=file["v6addr"]) + "/64"
            node.wgAddress = random_v4_addr(network=file["wg_addr"]) + "/16"
            node.PrivateKey, node.PublicKey = genkey()
            node.AllowedIPs = node.wgAddress[:-2] + "32"
            #node = Node(Name = {node.Name:node.__dict__})
            #node = {node.Name: node.__dict__}

            with open(f"{filename}/{filename}.json", "r+") as f:
                file = json.load(f)
                file["nodelist"][f"{node.Name}"] = node.__dict__
                f.seek(0)
                json.dump(file, f)
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



        

