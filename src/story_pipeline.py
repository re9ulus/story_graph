import file_ops
from book_ops import BookOps
import graph_ops
import sentiment_ops

PATH_TO_BOOK = './../books/harry.txt ' #'./../books/storm_of_swords.txt'
PATH_TO_NAMES_FILE = './../tmp_files/hero_names.txt'
PATH_TO_CLEARED_NAMES_FILE = './../tmp_files/test_hp_names.txt' #'./../tmp_files/test_st_of_sw_names.txt'
PATH_TO_NAME_POSITIONS_FILE = './../tmp_files/test_positions.txt'
PATH_TO_GRAPH = './../tmp_files/test_graph.vna'

WORDS_DISTANCE = 6
MIN_OCCURANCE = 5

# TODO: Current implementation uses a lot of file ops for testing, remove them
# TODO: Match different names to one character

def get_words():
	'''get words from book
	'''
	raw_text = file_ops.load_text_from_file(PATH_TO_BOOK)
	book_text = book_ops.remove_punctuation_from_text(raw_text)
	words = book_ops.text_to_words(book_text)
	return words


def book_to_names(book):
	'''get names from the words
	'''
	names = b.get_names_from_text()
	file_ops.save_names_to_file(PATH_TO_NAMES_FILE, names)
	return names


def word_positions_for_names(book):
	'''get word positions from the names and words
	'''
	# TODO: Remove this later, and use words as arguments  
	# words = book._words #get_words()

	names = file_ops.load_names_from_file(PATH_TO_CLEARED_NAMES_FILE)
	word_positions = {}
	for name, _c in names.iteritems():
		word_positions[name] = book.get_all_token_positions(name)
	file_ops.save_token_positions_to_file(PATH_TO_NAME_POSITIONS_FILE, word_positions)
	return word_positions


def build_graph(book):
	'''build graph from word positions
	'''
	name_positions = file_ops.load_token_positions_from_file(PATH_TO_NAME_POSITIONS_FILE)
	g = graph_ops.Graph()
	connections = b.get_connection_powers(name_positions, WORDS_DISTANCE) #get_connections(name_positions, WORDS_DISTANCE)
	
	for conn, count in connections.iteritems():
		g.add_connection(*conn)
		g.set_connection_weight(conn, count)

	names = file_ops.load_names_from_file(PATH_TO_CLEARED_NAMES_FILE)
	for name, count in names.iteritems():
		g.set_node_weight(name, count)

	print g._repr_with_weights()
	print '\n\n\n'
	print g.__repr__()

	return g


def get_sentiment_for_names(book):
	names = file_ops.load_names_from_file(PATH_TO_CLEARED_NAMES_FILE)
	i = 0
	res = []
	join_st = lambda s: ' '.join(s)
	for name, _c in names.iteritems():
		# if i > 5:
		# 	break
		name_occurances = book.get_all_token_positions(name)
		name_surrs = book.get_all_positions_surroundings(name_occurances, delta=3)
		name_surrs = map(join_st, name_surrs)
		# print name_surrs[:10]
		res.append((sentiment_ops.estimate_for_list(name_surrs), name))
		i += 1
	for val, name in sorted(res):
		print '{0}:\t\t{1}'.format(name, val)


if __name__ == '__main__':
	raw_text = file_ops.load_text_from_file(PATH_TO_BOOK)
	b = BookOps(text=raw_text, use_stemmer=True, min_occurance=MIN_OCCURANCE)
	# book_to_names(b)

	word_pos = word_positions_for_names(b)
	get_sentiment_for_names(b)

	# g = build_graph(b)
	# g.save_graph_to_vna(PATH_TO_GRAPH)
