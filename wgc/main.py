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

    def main(self):
       node = Node(**self.wgc_info())
       return to_toml(node).replace('"', "")

if __name__ == "__main__":
    a = wgc()
    a.main()
