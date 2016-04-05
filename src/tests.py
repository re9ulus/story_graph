# TODO: 
# 1. Stemming/lemmatization of the file (for names may be unnecessary, becouse they are unchanged)
# 2. Find all words that start with capital later, when previous letter wasn't in '.!?' (sentance end)
# 3. Remove all non ascii characters from book
# 4. Think about functions that accepts already splitted text, to avoid splitting in evety function
#

import string

def get_names(text):
	'''
	text -> [(string, int)], (name, frequency) sorted by frequency
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


# Trying to get words that are not the beginning of the sentance
def get_names_v2():
	'''
	text -> [(string, int)], (name, frequency) sorted by frequency
	'''
	for word in words:
		if word in words_occurance:
			words_occurance[word] += 1
		else:
			words_occurance[word] = 1
	words_occurance = zip(words_occurance.keys(), words_occurance.values())
	words_occurance = sorted(words_occurance, key=lambda item: item[1], reverse=True)
	return words_occurance


def lemmatization(text):
	'''
	text -> text, make text lemmatization
	'''
	raise Exception('Not implemented')


def clear(text):
	'''
	text -> text, remove all punctuation from the text
	''' 
	raise Exception('Not implemented')


def count_occurance(text, token):
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


def prepare_text(text):
	'''
	string -> string, convert the text, remove all puncutation
	'''
	exclude = set(string.punctuation)
	return ''.join(ch for ch in text if ch not in exclude)


if __name__ == '__main__':
	prepared_book_path = 'test_result.txt'

	raw_text = get_text('../books/storm_of_swords.txt')
	book_text = prepare_text(raw_text)

	with open(prepared_book_path, 'w+') as f:
		f.write(book_text)
	words_occurance = get_names(book_text)
	with open('get_names.txt', 'w+') as f:
		for occurance in words_occurance:
			f.write('{0} : {1}\n'.format(occurance[0], occurance[1]))

	print(count_occurance(book_text, 'Sansa'))
