from utils import *
from config import *
from pathlib import Path

def network(name:str="wg0"):
    
    if Path("{}".format(name)).is_file():
        raise OSError("This configuration exists in local directory")
    else:
        network = Network()
        network_info = "[Network]\n" + to_toml(network)
        with open("{}.conf".format(name), "w") as f:
            f.write(network_info)
        return 0

def node(name:str="wg0"):
    network = from_toml(Network, open("wg0.conf", "r").read())
    node = Node()
    node.Name = names.get_first_name()
    node.Address = network.addr4Pool[:-4] + str(random.randint(1, 255)) + "/24"
    node.ListenPort = random.randint(32768, 60999)
    node.Privatekey, node.PublicKey = wgc_genkey()
    AllowedIPs = node.Address[:-2] + "/32"
    node_info = "\n[Node.{}]\n".format(node.Name) + to_toml(node)
    with open("{}.conf".format(name), "a") as f:
        f.write(node_info)
    return 0
        
