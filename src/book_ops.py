import re
import math
import string
from collections import Counter

from nltk.stem.snowball import SnowballStemmer


def is_capitalized(word):
	return len(word) and word[0].isupper()


def text_to_words(text):
	'''convert text to separate words

	text -> [string]
	'''
	return text.split()


def remove_punctuation_from_text(text):
	'''remove punctuation from text

	string -> string
	remove all puncutation
	'''
	exclude = set(string.punctuation)
	return ''.join(ch for ch in text if ch not in exclude)


def remove_punctuation_from_words(words):
	'''remove punctuation from each word

	[string] -> string
	remove all puncutation
	'''
	return list(map(remove_punctuation_from_text, words))


def get_stemmer():
	'''get standard stemmer to use in all book_ops functions'''
	return SnowballStemmer('english')


# TODO: Add tests for stemming functions
# TODO: Add stemming to get_connections function

def stem_string(text):
	'''stem text

	string -> string
	'''
	return get_stemmer().stem(text)


def get_stem_words_dict(names):
	'''get dict of stemmed words to original words

	[string] -> {string: string}
	'''
	stemmer = get_stemmer()
	stemmed_words = {}
	for name in names:
		stemmed = stemmer.stem(name)
		# based on the assumption that the first occurrence of the name will be without 's' at the end. Don't change
		if stemmed not in stemmed_words:
			stemmed_words[stemmed] = name
	return stemmed_words


def stem_words(words):
	'''stem list of words

	[string] -> [string]
	'''
	stemmer = get_stemmer()
	return map(stemmer.stem, words)


def get_names_from_words(words, min_occurance=0):
	'''get dict of names in the list of words

	[string] -> {string: int}
	name - is capitaliazed word.
	dict key is name
	dict value is number of occurances of the name in text
	'''
	# TODO: Add "use stemmer to this function"
	names = filter(is_capitalized, words)
	words_occurance = Counter(names)
	if min_occurance > 0:
		words_occurance = {k: v for k, v in words_occurance.iteritems() if v > min_occurance}
	return words_occurance


def get_names_from_text(text, min_occurance=0, use_stemmer=True):
	'''get dict of names in the text

	string -> {string: int}
	name - is capitaliazed word.
	dict key is name
	dict value is number of occurances of the name in text
	'''
	name_pattern = '[^\.\!\?\"]\s+([A-Z][a-z]+)'
	names = set(re.findall(name_pattern, text))
	words = filter(is_capitalized, text_to_words(remove_punctuation_from_text(text)))

	if use_stemmer:
		stem_words_dict = get_stem_words_dict(names)
		names = stem_words(names)
		words = stem_words(words)

	words_occurance = Counter()
	for word in words:
		if word in names:
			words_occurance[word] += 1

	if use_stemmer:
		words_occurance = {stem_words_dict[name]: words_occurance[name] for name in names}

	if min_occurance > 0:
		words_occurance = {k: v for k, v in words_occurance.iteritems() if v > min_occurance}

	return words_occurance


def get_all_token_positions(words, token):
	'''get all positions of the token in the string array

	[string] -> [int]
	'''
	return [i for i, word in enumerate(words) if word == token]


def count_token_occurrence(words, token):
	'''find number of occurances of the token in string array

	[string], string -> int
	'''
	return words.count(token)


def count_tokens_within_distance(token1_pos, token2_pos, dist):
	'''count number of occurrences token1 within distance to token2

	[int], [int], dist -> [int]
	'''
	score = 0
	for i in token1_pos:
		for j in token2_pos:
			if abs(i - j) <= dist:
				score += 1
			elif j > i and abs(i - j) > dist:
				break
	return score


def get_connection_powers(name_occurances, dist):
	'''get connections and they powers from {name, [positions]} dict

	{string, [int]}, int -> {(string, string), int}
	'''
	connections = {}
	for name1, positions1 in name_occurances.iteritems():
		for name2, positions2 in name_occurances.iteritems():
			key = tuple(sorted((name1, name2)))
			if name1 == name2 or key in connections:
				continue
			else:
				conn_power = count_tokens_within_distance(positions1, positions2, dist)
				if conn_power > 0:
					connections[key] = conn_power
	return connections


def get_connections(name_occurances, dist):
	'''get connections from {name: [positions]} dict

	{string: [int]}, int -> [(string, string)]
	'''
	connections = []
	connection_powers = get_connection_powers(name_occurances, dist)
	for connection, power in connection_powers.iteritems():
		if power > 0:
			connections.append(connection)
	return connections
