import file_ops
import book_ops

PATH_TO_BOOK = './../books/storm_of_swords.txt'
PATH_TO_NAMES_FILE = './hero_names.txt'
PATO_TO_CLEARED_NAMES_FILE = './test_st_if_sw_name.txt'

# 1. Get list of heros +
# 2. Clean list of heros +
# 3. Get power of connectionw btw heros
# 4. Build graph

# TODO: Match different names to one character

def book_to_names():
	raw_text = file_ops.load_text_from_file(PATH_TO_BOOK)
	book_text = book_ops.remove_punctuation_from_text(raw_text)
	words = book_ops.text_to_words(book_text)
	names = book_ops.get_names(words)
	file_ops.save_names_to_file(PATH_TO_NAMES_FILE, names)


def word_positions_for_names():



if __name__ == '__main__':
	book_to_names()

