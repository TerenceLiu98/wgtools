from utils import *

class wgc(object):
    def __init__(self):
        pass

    def wgc_info(self):
        key = wgc_genkey()
        ipv4 = wgc_ipv4()
        info = {"Address": ipv4}
        info = {**key, **info}
        return info 

    def network(self):
       node = Node(**self.wgc_info())
       toml_struct = "[Network-{}]\n".format(names.get_first_name()) +to_toml(node).replace('"', "")
       with open("wg_vpn.conf", "w") as f:
           f.write(toml_struct)


if __name__ == "__main__":
    a = wgc()
    a.network()
