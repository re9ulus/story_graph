import file_ops
import book_ops
import graph_ops

PATH_TO_BOOK = './../books/storm_of_swords.txt'
PATH_TO_NAMES_FILE = './../tmp_files/hero_names.txt'
PATH_TO_CLEARED_NAMES_FILE = './../tmp_files/test_st_of_sw_names.txt'
PATH_TO_NAME_POSITIONS_FILE = './../tmp_files/test_st_of_sw_positions.txt'

WORDS_DISTANCE = 6

# 1. Get list of heros +
# 2. Clean list of heros +
# 3. Get power of connectionw btw heros +
# 4. Build graph +

# TODO: Current implementation uses a lot of file ops for testing, remove them
# TODO: Match different names to one character

def get_words():
	'''get words from book
	'''
	raw_text = file_ops.load_text_from_file(PATH_TO_BOOK)
	book_text = book_ops.remove_punctuation_from_text(raw_text)
	words = book_ops.text_to_words(book_text)
	return words


def book_to_names():
	'''get names from the words
	'''
	words = get_words()
	names = book_ops.get_names(words)
	file_ops.save_names_to_file(PATH_TO_NAMES_FILE, names)
	return names


def word_positions_for_names():
	'''get word positions from the names and words
	'''
	# TODO: Remove this later, and use words as arguments  
	words = get_words()

	names = file_ops.load_names_from_file(PATH_TO_CLEARED_NAMES_FILE)
	word_positions = {}
	for name, _c in names.iteritems():
		word_positions[name] = book_ops.get_all_token_positions(words, name)
	file_ops.save_token_positions_to_file(PATH_TO_NAME_POSITIONS_FILE, word_positions)
	return word_positions_for_names


def build_graph():
	'''build graph from word positions
	'''
	name_positions = file_ops.load_token_positions_from_file(PATH_TO_NAME_POSITIONS_FILE)
	g = graph_ops.Graph()
	connections = book_ops.get_connection_powers(name_positions, WORDS_DISTANCE) #get_connections(name_positions, WORDS_DISTANCE)
	
	for conn, count in connections.iteritems():
		g.add_connection(*conn)
		g.set_connection_weight(conn, count)

	names = file_ops.load_names_from_file(PATH_TO_CLEARED_NAMES_FILE)
	for name, count in names.iteritems():
		g.set_node_weight(name, count)

	# print g.__repr__()
	print g._repr_with_weights()
	# TODO: Write graph to file to file
	print '\n\n\n'
	print g.__repr__()

	return g


if __name__ == '__main__':
	# book_to_names()
	word_positions_for_names()
	g = build_graph()
	# g.save_graph_to_file('./../graph_vis/js/test_graph.js')
	g.save_graph_to_csv('test_graph.csv')
