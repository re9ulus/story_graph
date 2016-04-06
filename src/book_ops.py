
def get_all_token_positions(text, token):
	'''
	text -> [int], all positions of token in the text
	'''
	words = text.split()
	return [i for i, word in enumerate(words) if word == token]


def count_token_occurrence(text, token):
	'''
	text, string -> int, find the number of occurances of the string in the text
	'''
	words = text.split()
	return words.count(token)


def get_text(path_to_book):
	'''
	string -> string, read book text from the book
	'''
	with open(path_to_book, 'r') as book:
		result = book.read()
	return result
