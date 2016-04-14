import unittest
import graph_ops


class TestGraphOps(unittest.TestCase):

	def test_graph_creation1(self):
		g = graph_ops.Graph()
		self.assertEqual(g._graph, {})

	def test_graph_add_node1(self):
		g = graph_ops.Graph()
		g.add_node('A')
		g.add_node('B')
		self.assertEqual(g._graph, {'A': set(), 'B': set()})

	def test_graph_add_node2(self):
		g = graph_ops.Graph()
		g.add_node('A')
		g.add_node('A')
		self.assertEqual(g._graph, {'A': set()})

	def test_graph_add_connecion1(self):
		g = graph_ops.Graph()
		g.add_connection('A', 'B')
		g.add_connection('A', 'C')
		self.assertEqual(g._graph, {'A': set(['B', 'C']), 'B': set('A'), 'C': set('A')})

	def test_graph_add_connecion2(self):
		g = graph_ops.Graph()
		g.add_node('A')
		g.add_node('B')
		g.add_connection('A', 'B')
		g.add_connection('A', 'C')
		self.assertEqual(g._graph, {'A': set(['B', 'C']), 'B': set('A'), 'C': set('A')})

	def test_graph_is_node_in1(self):
		g = graph_ops.Graph()
		self.assertEqual(g.is_node_in_graph('A'), False)

	def test_graph_is_node_in2(self):
		g = graph_ops.Graph()
		g.add_node('A')
		self.assertEqual(g.is_node_in_graph('A'), True)

if __name__ == '__main__':
	unittest.main()
