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
		"PrivateKey": "", # drop this before post/put
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

class Client(object):

	def __init__(self, url):
		self.url = url
		with open("node.json", "r") as f:
			self.node_info = json.load(f)
			f.close()
		self.node_info["node"].pop("PrivateKey")

	def get(self):
		re = requests.get(self.url)
		response = re.json()
		return response["nodes"]

	def put(self):
		re = requests.get(self.url, json=node_info)
		response = re.json()
		return response

	def post(self):
		re = requests.post(self.url, json=node_info)
		response = re.json()
		return response

	def delete(self):
		re = requests.delete(self.url, json=node_info)
		response = re.json()
		return response