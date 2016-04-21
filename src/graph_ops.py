from collections import defaultdict

class Graph:
	'''Implementation of unoredered graph

	node is string
	connection is (node1, node2)
	'''

	def __init__(self):
		self._graph = {}
		self._node_weights = defaultdict(int)
		self._connection_weights = defaultdict(int)

	def add_node(self, node):
		if node not in self._graph:
			self._graph[node] = set()

	def add_connection(self, node1, node2):
		self.add_node(node1)
		self.add_node(node2)
		self._graph[node1].add(node2)
		self._graph[node2].add(node1)

	def is_node_in_graph(self, node):
		return node in self._graph

	def is_connection_in_graph(self, connection):
		node1, node2 = connection
		self._check_node_in_graph_error(node1)
		self._check_node_in_graph_error(node2)
		return node2 in self._graph[node1]

	def get_node_degree(self, target_node):
		self._check_node_in_graph_error(target_node)
		degree = 0
		for node, connections in self._graph.iteritems():
			if node == target_node:
				continue
			if target_node in connections:
				degree += 1
		return degree

	def get_node_connections(self, node):
		self._check_node_in_graph_error(node)
		return self._graph[node]

	def set_node_weight(self, node, weight):
		self._check_node_in_graph_error(node)
		self._node_weights[node] = weight

	def get_node_weight(self, node):
		self._check_node_in_graph_error(node)
		return self._node_weights[node]

	def set_connection_weight(self, connection, weight):
		'''set weight to connection'''
		self._check_connection_in_graph_error(connection)
		self._connection_weights[self._connection_key(connection)] = weight

	def get_connection_weight(self, connection):
		'''set weight to connection'''
		self._check_connection_in_graph_error(connection)
		return self._connection_weights[self._connection_key(connection)]

	def save_graph_to_file(self, path_to_file):
		raise Exception('Not implemented')

	def load_graph_from_file(self, path_to_file):
		raise Exception('Not implemented')

	def __repr__(self):
		res = 'graph: \n'
		for node, connections in sorted(self._graph.iteritems()):
			res += '{0} : {1}\n'.format(node, connections)
		return res

	def _check_node_in_graph_error(self, node):
		if not self.is_node_in_graph(node):
			raise ValueError('node {0} not found'.format(node))

	def _check_connection_in_graph_error(self, connection):
		if not self.is_connection_in_graph(connection):
			raise ValueError('connection {0} not found'.format(node))

	def _connection_key(self, connection):
		'''represent connection in order used in inner dicts'''
		return tuple(sorted(connection))
