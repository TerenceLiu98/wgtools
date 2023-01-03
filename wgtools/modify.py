#!/usr/bin/env python3

import sys
import json

def main(filename:str="wg0", nodename:str="node1", param:str="Endpoint", value:str=None):
    if value == None:
        raise ValueError("Value cannot be empty.")
    else:
        with open(f"{filename}/{filename}.json", "r+") as f:
            config = json.load(f)
            f.close()
        config["nodelist"][nodename][param] = value
        with open(f"{filename}/{filename}.conf", "w") as f:
            json.dump(f)
        return None

if __name__ == "__main__":
    if len(sys.argv) < 2:
        """
        print usable argument
        """
        raise ValueError("Command is needed")
        sys.exit()
    else:    
        main(filename=sys.argv[1], nodename=sys.argv[2], param=sys.argv[3], value=sys.argv[4])
