from collections import defaultdict
from Queue import PriorityQueue

class Graph:
    """Implementation of unoredered graph

    node is string
    connection is (node1, node2)
    """

    def __init__(self):
        self._graph = {}
        self._node_weights = defaultdict(int)
        self._connection_weights = defaultdict(int)
        self._connection_sentiment_weights = defaultdict(int)

    def _clear(self):
        self._graph = {}
        self._node_weights = defaultdict(int)
        self._connection_weights = defaultdict(int)
        self._connection_sentiment_weights = defaultdict(int)

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
        """set weight to connection
        """
        self._check_connection_in_graph_error(connection)
        self._connection_weights[self.connection_key(connection)] = weight

    def get_connection_weight(self, connection):
        """get connection weight
        """
        self._check_connection_in_graph_error(connection)
        return self._connection_weights[self.connection_key(connection)]

    def set_connection_sentiment(self, connection, weight):
        # TODO: Add tests
        """set connection sentiment
        """
        self._check_connection_in_graph_error(connection)
        self._connection_sentiment_weights[self.connection_key(connection)] = weight

    def get_connection_sentiment(self, connection):
        """get connection sentiment"""
        self._check_connection_in_graph_error(connection)
        return self._connection_sentiment_weights[
            self.connection_key(connection)]

    def central_metric(self, node):
        """return node central metric
        """
        raise Exception('Not implemented')

    def __repr__(self):
        res = 'graph: \n'
        for node, connections in sorted(self._graph.iteritems()):
            res += '{0} : {1}\n'.format(node, connections)
        return res

    def repr_with_weights(self):
        res = 'graph: \n'
        for node, connections in sorted(self._graph.iteritems()):
            res += '{0} : {1}\n'.format(node, self.get_node_weight(node))
            for conn in connections:
                res += '\t{0} : {1}\n'.format(conn, self.get_connection_weight((node, conn)))
        return res

    def _check_node_in_graph_error(self, node):
        if not self.is_node_in_graph(node):
            raise ValueError('node {0} not found'.format(node))

    def _check_connection_in_graph_error(self, connection):
        if not self.is_connection_in_graph(connection):
            raise ValueError('connection {0} not found'.format(connection))

    @staticmethod
    def connection_key(connection):
        """represent connection in order used in inner dicts"""
        return tuple(sorted(connection))

    def get_nodes(self):
        """get list of all nodes in graph"""
        return self._graph.keys()

    def get_connections(self):
        """get list of all connections in graph"""
        connections = set()
        for start_node in self.get_nodes():
            end_nodes = self.get_node_connections(start_node)
            for end_node in end_nodes:
                connections.add(tuple(sorted([start_node, end_node])))
        return list(connections)

    def get_graph(self):
        return self._graph

    def init_from_book(self, book, distance=6):
        """build graph from BookOps
        """
        # TODO: Refactor later, when get_conneciton_powers will be a class method (remove distance)
        self._clear()
        name_positions = book.all_names_positions()
        connections = book.get_connection_powers(name_positions, distance)
        for conn, count in connections.iteritems():
            self.add_connection(*conn)
            self.set_connection_weight(conn, count)
        for name, count in book.get_names().iteritems():
            self.set_node_weight(name, count)
        return self

    def max_spanning_tree(self):
        """
        Kruskal's algorithm for min spanning tree, to get most important
        connections in graph.
        -> Graph
        """
        # TODO: Test
        # TODO: Add unit tests
        pq = PriorityQueue()

        for conn in self.get_connections():
            # Hack negative number used to get use priority queue in inverse order
            # (to get max values first)
            pq.put((-self.get_connection_weight(conn), self.connection_key(conn)))

        min_tree = Graph()
        while not pq.empty():
            curr_weight, curr_connection = pq.get()
            curr_weight = -curr_weight # Hack with negative number
            if min_tree.is_node_in_graph(curr_connection[0]) and \
                min_tree.is_node_in_graph(curr_connection[1]):
                continue

            min_tree.add_connection(*curr_connection)
            min_tree.set_connection_weight(curr_connection, curr_weight)

        for node in self.get_nodes():
            min_tree.set_node_weight(node, self.get_node_weight(node))

        return min_tree


class GraphIO:

    def __init__(self):
        pass

    @staticmethod
    def save_graph_to_vna(g, path_to_file):
        nodes = g.get_graph().keys()
        edges = set()
        for node, connections in g.get_graph().iteritems():
            for conn in connections:
                edges.add(g.connection_key((node, conn)))
        edges = list(edges)
        edges = map(list, edges)
        with open(path_to_file, 'w+') as f:
            f.write('*node data\n')
            f.write('ID count\n')
            for node in nodes:
                f.write('{0} {1}\n'.format(node, g.get_node_weight(node)))
            f.write('*tie data\n')
            f.write('from to strength sentiment\n')
            for edge in edges:
                f.write('{0} {1} {2} {3}\n'.format(edge[0], edge[1],
                                                   g.get_connection_weight(edge),
                                                   g.get_connection_sentiment(edge)))

    @staticmethod
    def save_graph_to_file(g, path_to_file):
        nodes = g.get_graph().keys()
        edges = set()
        for node, connections in g.get_graph().iteritems():
            for conn in connections:
                edges.add(g.connection_key((node, conn)))
        edges = list(edges)
        edges = map(list, edges)
        with open(path_to_file, 'w+') as f:
            f.write('var nodes = ' + str(nodes) + ';\n')
            f.write('var edges = ' + str(edges) + ';\n')

    @staticmethod
    def save_graph_to_csv(g, path_to_file):
        edges = set()
        for node, connections in g.get_graph().iteritems():
            for conn in connections:
                edges.add(g.connection_key((node, conn)))
        edges = list(edges)
        with open(path_to_file, 'w+') as f:
            for edge in edges:
                f.write('{0},{1}\n'.format(edge[0], edge[1]))

    @staticmethod
    def load_graph_from_file(g, path_to_file):
        raise Exception('Not implemented')
