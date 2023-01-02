# WG-Tools

A Tool of auto configuration generator of Wireguard.


## Features

* Automatrically select IP from the network pool assigned to client
* VXLAN over Wireguard - Full-mesh network configuration

## Design

1. Generate Network area: `python add.py netwrk areaA`
   1. randomly choose a ip addr for the area: `add.network` as the vxlan ip
   2. assign a reserved ip (`192.168.x.0/24`, where `x` in 200 - 254) to node for wireguard connection
2. while wireguard connection established, we also estabilish a vxlan as an overlay network

## Usage

* prerequest:
	* clone the code into local directory: `git clone  https://github.com/TerenceLiu98/wgtools.git`
	* install the requirement: `python -m pip install -r requirements.txt`
	* install the wireguard before using the tool

* configuration:
	* new a ipv4 pool: `python add.py network wg0`
	* new (a) peer(s): `python add.py node wg0 node1` + `python add.py node wg0 node2` + `python add.py node wg0 node3`
	* check the information: `cat wg0.conf`
	* modify the endpoint: `python modify.py wg0 node1 Endpoint 1.1.1.1`
	* generate configuration for each node: `python generate.py wg0 node1` + `python genenrate.py wg0 node2` + `python generate wg0 node3`

* script
	* copy the configuration to the machine
	* use `wg-quick` to quick start the wireguard
	* check the connectivity via `ping` (both wg ip and vxlan ip)

## Acknowledgement

* [VxWireguard-Generator](https://github.com/m13253/VxWireguard-Generator)
* [wireguard-doc(Unofficial)](https://github.com/pirate/wireguard-docs)

