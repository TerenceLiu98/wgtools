from utils import *
from database import *
from flask_restful import Resource, Api, reqparse

api = Api(app)

parser = reqparse.RequestParser()
parser.add_argument('node', type=dict, help='Node information', location="json") # node info with json

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

class Node_in_Namespace(Resource):
	def get(self, sid):
		namespace = Namespace.query.filter_by(sid=sid).first()
		nodes = []
		for i in range(0, len(namespace.nodes)):
			nodes.append(namespace.nodes[i])
		return jsonify(nodes=nodes)

	def put(self, sid):
		args = parser.parse_args()
		node_info = args["node"]
		if bool(Node.query.filter_by(nid=node_info["nid"]).first()):
			node = Node.query.filter_by(nid=node_info["nid"]).first()
			for k, v in node_info.items():
				if k in node.__dict__ and node_info[k] != v:
					new_node = Node(**node_info)
					database.session.delete(node)
					database.session.add(new_node)
					database.session.commit()
					return jsonify(response="Node updated")
				else:
					return jsonify(response="Same information, no need to update")

	def post(self, sid):
		args = parser.parse_args()
		node_info = args["node"]
		if bool(Node.query.filter_by(nid=node_info["nid"]).first()):
			return jsonify(response="Node exists")
		elif check_node(new_node=node_info) != True:
			return jsonify(response="IP Address duplicated")
		else:
			node = Node(**node_info)
			database.session.add(node)
			database.session.commit()
			return jsonify(response="Node added")

	def delete(self, sid):
		args = parser.parse_args()
		node_info = args["node"]
		if bool(Node.query.filter_by(nid=node_info["nid"]).first()):
			node = Node.query.filter_by(nid=node_info["nid"]).first()
			database.session.delete(node)
			database.session.commit()
			return jsonify(response="Node deleted")

		

api.add_resource(Node_in_Namespace, "/api/node/<int:sid>")

if __name__ == '__main__':
    app.run(debug=True)