import string

def get_names(text):
	'''get (name, frequency) sorted by frequency from the text

	text -> [(string, int)]
	'''
	is_capitalized = lambda word: len(word) and word[0].isupper()
	words = filter(is_capitalized, text.split())
	words_occurance = {}
	for word in words:
		if word in words_occurance:
			words_occurance[word] += 1
		else:
			words_occurance[word] = 1
	words_occurance = zip(words_occurance.keys(), words_occurance.values())
	words_occurance = sorted(words_occurance, key=lambda item: item[1], reverse=True)
	return words_occurance


def get_text(path_to_book):
	'''read book text from the file

	string -> string
	'''
	with open(path_to_book, 'r') as book:
		result = book.read()
	return result


def prepare_text(text):
	'''prepare text for processing

	string -> string
	remove all puncutation
	'''
	exclude = set(string.punctuation)
	return ''.join(ch for ch in text if ch not in exclude)



def get_all_token_positions(text, token):
	'''get all positions of the token in the text

	text -> [int]
	'''
	words = text.split()
	return [i for i, word in enumerate(words) if word == token]


def count_token_occurrence(text, token):
	'''find number of occurances of the token in the text

	text, string -> int
	'''
	words = text.split()
	return words.count(token)


def text_to_words(text):
	'''convert text to separate words

	text -> [string]
	'''
	return text.split()
