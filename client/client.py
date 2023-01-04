import json
import requests

"""
client json design
{
	"node": {
		"nid": "uuid",
        "sid": "uuid",
		"Name": "name",
		"v4Address": "",
		"v6Address": "",
		"wgAddress": "",
		"MTU": 0,
		"ListenPort": 0,
		"PublicKey": "",
		"Endpoint": "",
		"AllowedIPs": "",
		"PersistentKeepalive": 0
    }
    "peers": {
		"peer1": {
			"nid": "uuid",
            "Name": "name",
			"wgAddress": "",
			"ListenPort": 0,
			"PublicKey": "",
			"Endpoint": "",
			"AllowedIPs": "",
			"PersistentKeepalive": 0
		},
	}
        
}
"""

"""
get: https://<URL>/api/node/?ns=<namespace>&uuid=<uuid>
post: https://<URL>/api/node/<namespace>
"""

def get_peer(url, namespace, uuid):
    re = requests.get(url, params={"ns": namespace, "uuid": uuid})
    re.status_code
    return re.json()

def push_info(url, node_info):
    re = requests.post(url, json=node_info)
    return re.json()

def main(url):
    with open("node.json", "r") as f:
        node_info = json.load(f)
        f.close()
    push_info = push_info(url, node_info)
    peer_info = get_peer(url, namespace=node_info["node"]["sid"], uuid=node_info["node"]["nid"])
    with open("node.json", "r+") as f:
        node_info = json.load(f)
        for i in range(0, len(peer_info["nodes"])):
            if peer_info["nodes"][i]["nid"] not in node_info["peerlist"]:
                node_info["peerlist"][peer_info["nodes"][i]["nid"]] = peer_info["nodes"][i]
                f.seek(0)
                json.dump(node_info, f)
            else:
                pass
        f.close()