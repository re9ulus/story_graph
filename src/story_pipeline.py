import file_ops
from book_ops import BookOps
import graph_ops
import sentiment_ops

PATH_TO_BOOK = './../books/storm_of_swords.txt ' #'./../books/harry.txt'
PATH_TO_NAMES_FILE = './../tmp_files/hero_names.txt' #'
PATH_TO_CLEARED_NAMES_FILE = './../tmp_files/sos_names.txt' #'./../tmp_files/test_st_of_sw_names.txt'
PATH_TO_GRAPH = './../tmp_files/test_graph.vna'

WORDS_DISTANCE = 6
MIN_OCCURANCE = 5

# TODO: Match different names to one character

join_st = lambda s: ' '.join(s)


def book_to_names(book):
	'''get names from the words
	'''
	file_ops.save_names_to_file(PATH_TO_NAMES_FILE, b.get_names_from_text())


def build_graph(book):
	'''build graph from word positions
	'''
	name_positions = book.all_names_positions()
	g = graph_ops.Graph()
	connections = b.get_connection_powers(name_positions, WORDS_DISTANCE)
	
	for conn, count in connections.iteritems():
		g.add_connection(*conn)
		g.set_connection_weight(conn, count)

	for name, count in book.get_names().iteritems():
		g.set_node_weight(name, count)

	print g._repr_with_weights()
	print '\n\n\n'
	print g.__repr__()

	return g


def get_connection_sent(book, conn):
	# TODO: Insert to class
	connection_positions = book.get_all_connection_positions(*conn, dist=5)
	connection_surrs = map(join_st, book.get_all_positions_surroundings(connection_positions, delta=5))
	return sentiment_ops.estimate_for_list(connection_surrs)


def build_graph_with_sentiment(book):
	'''build graph from word positions with sentiment connection
	'''
	name_positions = book.all_names_positions()
	g = graph_ops.Graph()
	connections = b.get_connection_powers(name_positions, WORDS_DISTANCE)
	
	for conn, count in connections.iteritems():
		g.add_connection(*conn)
		g.set_connection_weight(conn, count)
		sent = get_connection_sent(book, conn)
		g.set_connection_sentiment(conn, sent)

	for name, count in book.get_names().iteritems():
		g.set_node_weight(name, count)

	print g._repr_with_weights()
	print '\n\n\n'
	print g.__repr__()

	return g


def get_sentiment_for_names(book):
	res = []
	for name, _c in book.get_names().iteritems():
		name_occurances = book.name_positions(name)
		name_surrs = book.get_all_positions_surroundings(name_occurances, delta=3)
		name_surrs = map(join_st, name_surrs)
		res.append((sentiment_ops.estimate_for_list(name_surrs), name))
	for val, name in sorted(res):
		print('{0}:\t\t{1}'.format(name, val))
	print('')


def get_sentiment_for_connections(book, word_pos, target_name):
	'''target_name - character for whom get connection sentiments
	'''
	join_st = lambda s: ' '.join(s)
	res = []

	for name, _c in book.get_names().iteritems():
		if name == target_name:
			continue
		connection_positions = book.get_all_connection_positions(target_name, name, dist=WORDS_DISTANCE)
		connection_surrs = book.get_all_positions_surroundings(connection_positions, delta=5)
		connection_surrs = map(join_st, connection_surrs)

		res.append((sentiment_ops.estimate_for_list(connection_surrs), name))

	print('Sentiment for {0}:'.format(target_name))
	for val, name in sorted(res):
		print('{0}:\t\t{1}'.format(name, val))
	print('')


def merge_synonims(synonims_list, book):
	name_positions = book.all_names_positions()
	raise Exception('Not implemented')


GET_NAMES = False

if __name__ == '__main__':
	raw_text = file_ops.load_text_from_file(PATH_TO_BOOK)
	b = BookOps(text=raw_text, use_stemmer=True, min_occurance=MIN_OCCURANCE)
	if GET_NAMES:
		book_to_names(b)
	else:
		b.set_names(file_ops.load_names_from_file(PATH_TO_CLEARED_NAMES_FILE))

		# # get_sentiment_for_names(b)
		# # characters_to_test = ['Tyrion', 'Jaime', 'Sansa', 'Arya', 'Robb', 'Dany']
		# # for name in characters_to_test:
		# 	# get_sentiment_for_connections(b, word_pos, target_name = name)

		g = build_graph(b)
		# g = build_graph_with_sentiment(b)
		g.save_graph_to_vna(PATH_TO_GRAPH)
