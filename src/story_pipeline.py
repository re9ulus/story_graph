from functools import reduce

import file_ops
import graph_ops
import sentiment_ops
from book_ops import BookOps

import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

PATH_TO_BOOK = './../books/harry.txt'  # './../books/storm_of_swords.txt '
PATH_TO_NAMES_FILE = './../tmp_files/hero_names.txt' #
PATH_TO_CLEARED_NAMES_FILE = './../tmp_files/hero_names_got_1_5.txt'  # './../tmp_files/sos_names.txt'
PATH_TO_GRAPH = './../tmp_files/test_graph.vna'

WORDS_DISTANCE = 6
MIN_OCCURANCE = 50

GET_NAMES = False
WITH_SENTIMENT = True


# TODO: Add logging to functions
# TODO: Add graph saving to StoryToGraph class
# TODO: Insert synonyms list to names file
# graph_ops.GraphIO.save_graph_to_vna(g, PATH_TO_GRAPH)


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
        for conn, count in connections.items():
            sent = self._connection_sentiment(conn)
            self._graph.set_connection_sentiment(conn, sent)

    def demo_repr(self):
        print(self._graph.repr_with_weights())
        print('\n\n\n')
        print(self._graph.__repr__())

    def merge_synonims(self, synonyms):
        # TODO: Test
        """replace name synonyms in book
        synonyms : [[string]]
                   example: [['Harry', 'Potter'], ['Vernon', 'Uncle'], ['Snape', 'Severus']]
        """
        for syn_list in synonyms:
            self._book.merge_synonyms(syn_list)


def test_graph_build(books_paths, merge_books=False):
    logger.info('Test graph build')

    if merge_books:
        books = []
        for path in book_paths:
            logger.debug('book path: {}'.format(path))
            raw_text = file_ops.load_text_from_file(path)
            books.append(BookOps(text=raw_text, use_stemmer=WITH_SENTIMENT,
                                 min_occurance=100))
        b = reduce(BookOps.merge_books, books)
    else:
        raw_text = file_ops.load_text_from_file(PATH_TO_BOOK)
        b = BookOps(text=raw_text, use_stemmer=WITH_SENTIMENT, min_occurance=MIN_OCCURANCE)

    stg = StoryToGraph(book=b, words_distance=WORDS_DISTANCE, use_sentiment=WITH_SENTIMENT)

    if GET_NAMES:
        possible_names = stg.get_possible_names()
        stg.save_names_to_file(possible_names, PATH_TO_NAMES_FILE)
        return
    else:
        cleared_names = stg.read_names_from_file(PATH_TO_CLEARED_NAMES_FILE)
        stg.set_names(cleared_names)

        stg.merge_synonims([['Sam', 'Samwell'], ['Ned', 'Eddard'], ['Barristan', 'Selmy'],
                            ['Petyr', 'Littlefinger', 'Baelish'], ['Khal', 'Drogo'], ['Jaime', 'Kingslayer'],
                            ['Dany', 'Daenerys', 'Khaleesi']])

        stg.build_graph_with_sentiment() #build_graph()
        # stg.demo_repr()

    graph_ops.GraphIO.save_graph_to_vna(stg._graph, './../tmp_files/got_graph_1_5.vna')
    min_tree = stg._graph.prim() # max_spanning_tree()
    graph_ops.GraphIO.save_graph_to_vna(min_tree, './../tmp_files/got_tree_1_5.vna')

    # print('=== Min spanning tree ===')
    # print min_tree.repr_with_weights()
    # print '\n\n\n'
    # print min_tree.__repr__()

    graph_ops.GraphIO.save_graph_to_vna(min_tree, PATH_TO_GRAPH)


# def read_book_from_file(book_path):
#     if merge_books:
#         books = []
#         for path in book_paths:
#             logger.debug('book path: {}'.format(path))
#             raw_text = file_ops.load_text_from_file(path)
#             books.append(BookOps(text=raw_text, use_stemmer=WITH_SENTIMENT,
#                                  min_occurance=100))
#         b = reduce(BookOps.merge_books, books)
#     else:
#         raw_text = file_ops.load_text_from_file(PATH_TO_BOOK)
#         b = BookOps(text=raw_text, use_stemmer=WITH_SENTIMENT, min_occurance=MIN_OCCURANCE)

if __name__ == '__main__':
    MERGE_BOOKS = True
    book_paths = ['./../books/GoT{0}.txt'.format(i) for i in range(1, 6)]
    test_graph_build(book_paths, merge_books=MERGE_BOOKS)
