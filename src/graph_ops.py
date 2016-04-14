class Graph:

	def __init__(self):
		self._graph = {}

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

	def __repr__(self):
		res = 'graph: \n'
		for node, connections in sorted(self._graph.iteritems()):
			res += '{0} : {1}\n'.format(node, connections)
		return res
