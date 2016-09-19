import file_ops
import graph_ops
import sentiment_ops
from book_ops import BookOps

PATH_TO_BOOK = './../books/harry.txt'  # './../books/storm_of_swords.txt '
PATH_TO_NAMES_FILE = './../tmp_files/hero_names.txt'
PATH_TO_CLEARED_NAMES_FILE = './../tmp_files/hero_names.txt'  # './../tmp_files/sos_names.txt'
PATH_TO_GRAPH = './../tmp_files/test_graph.vna'

WORDS_DISTANCE = 6
MIN_OCCURANCE = 50

GET_NAMES = False
WITH_SENTIMENT = True


# TODO: Match different names to one character
# TODO: Add logging to functions

join_st = lambda s: ' '.join(s)


class StoryToGraph:

    def __init__(self, book, words_distance=6, use_sentiment=False):
        self._book = book
        self._use_sentiment = use_sentiment
        self._words_distance = words_distance
        self._graph = None

    def get_possible_names(self):
        return self._book.get_names_from_text()

    @staticmethod
    def save_names_to_file(names, filename):
        file_ops.save_names_to_file(names, filename)

    @staticmethod
    def read_names_from_file(filename):
        return file_ops.load_names_from_file(filename)

    def set_names(self, names):
        self._book.set_names(names)

    def build_graph(self):
        """build graph from word positions
        """
        self._graph = graph_ops.Graph()
        self._graph.init_from_book(self._book, self._words_distance)

    def _connection_sentiment(self, conn):
        connection_positions = self._book.all_connection_positions(*conn, dist=self._words_distance)
        connection_surrs = map(join_st, self._book.all_positions_surroundings(connection_positions,
                                                                              delta=self._words_distance))
        return sentiment_ops.estimate_for_list(connection_surrs)

    def build_graph_with_sentiment(self):
        """build graph from word positions with sentiment connection
        """
        self.build_graph()
        connections = self._book.get_connection_powers(self._book.all_names_positions(), self._words_distance)
        for conn, count in connections.iteritems():
            sent = self._connection_sentiment(conn)
            self._graph.set_connection_sentiment(conn, sent)

    def demo_repr(self):
        print self._graph.repr_with_weights()
        print '\n\n\n'
        print self._graph.__repr__()


def test_graph_build():

    USE_MERGE = False

    if USE_MERGE:
        book_paths = ['./../books/GoT{0}.txt'.format(i) for i in range(1, 3)]
        books = []
        for path in book_paths:
            print path
            raw_text = file_ops.load_text_from_file(path)
            books.append(BookOps(text=raw_text, use_stemmer=False,
                                 min_occurance=100))
        b = reduce(BookOps.merge_books, books)
    else:
        raw_text = file_ops.load_text_from_file(PATH_TO_BOOK)
        b = BookOps(text=raw_text, use_stemmer=True, min_occurance=MIN_OCCURANCE)

    stg = StoryToGraph(book=b, words_distance=WORDS_DISTANCE, use_sentiment=WITH_SENTIMENT)

    if GET_NAMES:
        possible_names = stg.get_possible_names()
        stg.save_names_to_file(PATH_TO_NAMES_FILE, possible_names)
    else:
        cleared_names = stg.read_names_from_file(PATH_TO_CLEARED_NAMES_FILE)
        stg.set_names(cleared_names)
        stg.build_graph()
        stg.demo_repr()

        # TODO: Add graph saving to StoryToGraph class
        # graph_ops.GraphIO.save_graph_to_vna(g, PATH_TO_GRAPH)


if __name__ == '__main__':
    test_graph_build()


# TODO: Implement in class
#  logic for name merging
#     synonims = [['Harry', 'Potter'], ['Vernon', 'Uncle'], ['Snape', 'Lucius']]
#     for syn_list in synonims:
#         b.merge_synonims(syn_list)
#
#



# Possible unneeded functions from tests

# def get_sentiment_for_names(book):
#     res = []
#     for name, _c in book.get_names().iteritems():
#         name_occurances = book.name_positions(name)
#         name_surrs = book.all_positions_surroundings(name_occurances, delta=3)
#         name_surrs = map(join_st, name_surrs)
#         res.append((sentiment_ops.estimate_for_list(name_surrs), name))
#     for val, name in sorted(res):
#         print('{0}:\t\t{1}'.format(name, val))
#     print('')


# def get_sentiment_for_connections(book, word_pos, target_name):
#     """target_name - character for whom get connection sentiments
#     """
#     res = []
#
#     for name, _c in book.get_names().iteritems():
#         if name == target_name:
#             continue
#         connection_positions = book.all_connection_positions(target_name, name, dist=WORDS_DISTANCE)
#         connection_surrs = book.all_positions_surroundings(connection_positions, delta=5)
#         connection_surrs = map(join_st, connection_surrs)
#         res.append((sentiment_ops.estimate_for_list(connection_surrs), name))
#
#     print('Sentiment for {0}:'.format(target_name))
#     for val, name in sorted(res):
#         print('{0}:\t\t{1}'.format(name, val))
#     print('')

