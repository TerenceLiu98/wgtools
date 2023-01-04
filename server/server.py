from utils import *
from database import *

# user flask as the api server for pushing configuration to each node
# each node has it uuid and based on the uuid we can push the configuration to the node
@app.route('/')
def index():
	return Response("Hello World", status=200, mimetype='application/json')


# client side get all other node's information with GET method
# client side push it's own information with POST method
def check_node(new_node): 
	sid = new_node["sid"]
	nodes_in_ns = Node.query.filter_by(sid=sid).all()
	v4addr_list = [node.v4Address for node in nodes_in_ns]
	v6addr_list = [node.v6Address for node in nodes_in_ns]
	wgaddr_list = [node.wgAddress for node in nodes_in_ns]
	if new_node["v4Address"] not in v4addr_list and new_node["v6Address"] not in v6addr_list and new_node["wgAddress"] not in wgaddr_list:
		return True
	else:
		return False

@app.route('/api/node/', methods=['GET', "POST"])
def node():
	if request.method == "GET":
		ns, uuid = request.args.get("ns"), request.args.get("nid")
		namespace = Namespace.query.filter_by(sid=1).first()
		nodes = []
		for i in range(0, len(namespace.nodes)):
			if namespace.nodes[i].nid != uuid:
				nodes.append(namespace.nodes[i])
		return jsonify(nodes=nodes)

	if request.method == "POST":
		content = request.json
		nid = content["nid"]
		if  bool(Node.query.filter_by(nid=nid).first()):
			return jsonify(response="Node exists")
		elif check_node(new_node=content) != True:
			return jsonify(response="IP Address duplicated")
		else:
			node = Node(**content)
			database.session.add(node)
			database.session.commit()
			return jsonify(response="Node added")


if __name__ == "__main__":
	database.create_all()
	app.run(debug=True)