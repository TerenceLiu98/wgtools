# WG-Tools

A Tool of auto configuration generator of Wireguard.


## Features

* Automatrically select IP from the network pool assigned to client
* Full-mesh network configuration

## Usage

* prerequest:
	* clone the code into local directory: `git clone  https://github.com/TerenceLiu98/wgtools.git`
	* install the requirement: `python -m pip install -r requirements.txt`
	* install the wireguard before using the tool

* configuration:
	* new a ipv4 pool: `python add.py network wg0`
	* new (a) peer(s): `python add.py wg0 node1` + `python add.py wg0 node2` + `python add.py wg0 node3`
	* check the information: `cat wg0.conf`
	* modify the endpoint: `python modify.py tun0 node1 Endpoint 1.1.1.1:11111`
	* generate configuration for each node: `python generate.py wg0 node1` + `python genenrate.py wg0 node2` + `python generate wg0 node3`

* script
	* copy the configuration to each machine
	* use `wg-quick` to quick start the wireguard
	* check the connectivity

## Acknowledgement

* [VxWireguard-Generator](https://github.com/m13253/VxWireguard-Generator)
* [wireguard-doc(Unofficial)](https://github.com/pirate/wireguard-docs)

