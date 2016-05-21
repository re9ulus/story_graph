import file_ops
from book_ops import BookOps
import graph_ops
import sentiment_ops

PATH_TO_BOOK = './../books/harry.txt'  # './../books/storm_of_swords.txt '
PATH_TO_NAMES_FILE = './../tmp_files/hero_names.txt'
PATH_TO_CLEARED_NAMES_FILE = './../tmp_files/hero_names.txt'  # './../tmp_files/sos_names.txt'
PATH_TO_GRAPH = './../tmp_files/test_graph.vna'

WORDS_DISTANCE = 6
MIN_OCCURANCE = 5

# TODO: Match different names to one character

join_st = lambda s: ' '.join(s)


def book_to_names(book):
    """get names from the words
    """
    file_ops.save_names_to_file(PATH_TO_NAMES_FILE, book.get_names_from_text())


def build_graph(book):
    """build graph from word positions
    """
    g = graph_ops.Graph()
    g.init_from_book(book, WORDS_DISTANCE)

    print g.repr_with_weights()
    print '\n\n\n'
    print g.__repr__()

    return g


def get_connection_sent(book, conn):
    # TODO: Insert to class
    connection_positions = book.all_connection_positions(*conn, dist=5)
    connection_surrs = map(join_st, book.all_positions_surroundings(connection_positions, delta=5))
    return sentiment_ops.estimate_for_list(connection_surrs)


def build_graph_with_sentiment(book):
    """build graph from word positions with sentiment connection
    """
    g = graph_ops.Graph()
    g.init_from_book(book, WORDS_DISTANCE)
    connections = book.get_connection_powers(book.all_names_positions(), WORDS_DISTANCE)

    for conn, count in connections.iteritems():
        sent = get_connection_sent(book, conn)
        g.set_connection_sentiment(conn, sent)

    print g.repr_with_weights()
    print '\n\n\n'
    print g.__repr__()

    return g


def get_sentiment_for_names(book):
    res = []
    for name, _c in book.get_names().iteritems():
        name_occurances = book.name_positions(name)
        name_surrs = book.all_positions_surroundings(name_occurances, delta=3)
        name_surrs = map(join_st, name_surrs)
        res.append((sentiment_ops.estimate_for_list(name_surrs), name))
    for val, name in sorted(res):
        print('{0}:\t\t{1}'.format(name, val))
    print('')


def get_sentiment_for_connections(book, word_pos, target_name):
    """target_name - character for whom get connection sentiments
    """
    res = []

    for name, _c in book.get_names().iteritems():
        if name == target_name:
            continue
        connection_positions = book.all_connection_positions(target_name, name, dist=WORDS_DISTANCE)
        connection_surrs = book.all_positions_surroundings(connection_positions, delta=5)
        connection_surrs = map(join_st, connection_surrs)

        res.append((sentiment_ops.estimate_for_list(connection_surrs), name))

    print('Sentiment for {0}:'.format(target_name))
    for val, name in sorted(res):
        print('{0}:\t\t{1}'.format(name, val))
    print('')


def merge_synonims(book, synonims_list):
    # TODO: Move logic to get_names_from_words, and get_names_from_text
    name_positions = book.all_names_positions()
    merged_list = []
    for name in synonims_list:
        print name, name_positions[name]
        merged_list += name_positions[name]
    merged_list = sorted(merged_list)
    res_list = []
    i = 0
    while i < len(merged_list)-1:
        if merged_list[i+1] - merged_list[i] < WORDS_DISTANCE:
            res_list.append((merged_list[i+1] + merged_list[i]) / 2)
            i += 1
        else:
            res_list.append(merged_list[i])
        i += 1

    book._names[synonims_list[0]] = len(res_list)
    map(book._names.pop, synonims_list[1:])

    print len(res_list)
    print len(merged_list)


GET_NAMES = False
WITH_SENTIMENT = True


def test_standard_graph_build():
    raw_text = file_ops.load_text_from_file(PATH_TO_BOOK)
    b = BookOps(text=raw_text, use_stemmer=True, min_occurance=MIN_OCCURANCE)
    if GET_NAMES:
        book_to_names(b)
    else:
        b.set_names(file_ops.load_names_from_file(PATH_TO_CLEARED_NAMES_FILE))

        # merge_synonims(b, ['Harry', 'Potter'])

        # # get_sentiment_for_names(b)
        # # characters_to_test = ['Tyrion', 'Jaime', 'Sansa', 'Arya', 'Robb', 'Dany']
        # # for name in characters_to_test:
        # 	# get_sentiment_for_connections(b, word_pos, target_name = name)

        if WITH_SENTIMENT:
            g = build_graph_with_sentiment(b)
        else:
            g = build_graph(b)

        graph_ops.GraphIO.save_graph_to_vna(g, PATH_TO_GRAPH)


def test_merge_graph_build():
    book_paths = ['./../books/GoT{0}.txt'.format(i) for i in range(1, 6)]
    books = []
    for path in book_paths:
        print path
        raw_text = file_ops.load_text_from_file(path)
        books.append(BookOps(text=raw_text, use_stemmer=True, min_occurance=50))
    b = reduce(BookOps.merge_books, books)

    if GET_NAMES:
        book_to_names(b)
    else:
        b.set_names(file_ops.load_names_from_file(PATH_TO_CLEARED_NAMES_FILE))

        if WITH_SENTIMENT:
            g = build_graph_with_sentiment(b)
        else:
            g = build_graph(b)

        graph_ops.GraphIO.save_graph_to_vna(g, PATH_TO_GRAPH)


if __name__ == '__main__':
    # test_standard_graph_build()
    test_merge_graph_build()