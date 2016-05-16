import unittest
import graph_ops
from collections import defaultdict

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

	def test_get_node_degree1(self):
		g = graph_ops.Graph()
		g.add_connection('A', 'B')
		g.add_connection('A', 'C')
		g.add_connection('B', 'D')
		g.add_connection('D', 'A')
		self.assertEqual(g.get_node_degree('A'), 3)
		self.assertEqual(g.get_node_degree('B'), 2)
		self.assertEqual(g.get_node_degree('C'), 1)
		self.assertEqual(g.get_node_degree('D'), 2)

	def test_get_node_connections1(self):
		g = graph_ops.Graph()
		g.add_node('A')
		self.assertEqual(g.get_node_connections('A'), set())

	def test_get_node_connections2(self):
		g = graph_ops.Graph()
		g.add_connection('A', 'B')
		g.add_connection('A', 'C')
		self.assertEqual(g.get_node_connections('A'), set(['B', 'C']))
		self.assertEqual(g.get_node_connections('B'), set(['A']))
		self.assertEqual(g.get_node_connections('C'), set(['A']))

	def test_get_node_weight1(self):
		g = graph_ops.Graph()
		g.add_node('A')
		self.assertEqual(g.get_node_weight('A'), 0)		

	def test_add_node_weight1(self):
		g = graph_ops.Graph()
		g.add_node('A')
		g.set_node_weight('A', 3)
		self.assertEqual(g.get_node_weight('A'), 3)

	def test_get_connection_weight1(self):
		g = graph_ops.Graph()
		g.add_connection('B', 'A')
		self.assertEqual(g.get_connection_weight(('A', 'B')), 0)
		self.assertEqual(g.get_connection_weight(('B', 'A')), 0)

	def test_set_connection_weight1(self):
		g = graph_ops.Graph()
		g.add_connection('B', 'A')
		g.set_connection_weight(('A', 'B'), 7)
		self.assertEqual(g.get_connection_weight(('A', 'B')), 7)
		self.assertEqual(g.get_connection_weight(('B', 'A')), 7)

	def test_is_connection_in_graph1(self):
		g = graph_ops.Graph()
		g.add_connection('A', 'B')
		self.assertTrue(g.is_connection_in_graph(('A', 'B')))
		self.assertTrue(g.is_connection_in_graph(('B', 'A')))

	def test_is_connection_in_graph1(self):
		g = graph_ops.Graph()
		g.add_node('A')
		g.add_node('B')
		self.assertFalse(g.is_connection_in_graph(('A', 'B')))
		self.assertFalse(g.is_connection_in_graph(('B', 'A')))

	def test_clear(self):
		g = graph_ops.Graph()
		g.add_connection('B', 'A')
		g.set_connection_weight(('A', 'B'), 7)
		g._clear()
		self.assertEqual(g._graph, {})
		self.assertEqual(g._node_weights, defaultdict(int))
		self.assertEqual(g._connection_weights, defaultdict(int))
		self.assertEqual(g._connection_sentiment_weights, defaultdict(int))


if __name__ == '__main__':
	unittest.main()
