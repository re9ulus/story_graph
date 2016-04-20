import math
import string

def get_names(words):
	'''get dict of names in the text

	[string] -> {string: int}
	name - is capitaliazed word.
	dict key is name
	dict value is number of occurances of the name in text
	'''
	is_capitalized = lambda word: len(word) and word[0].isupper()
	names = filter(is_capitalized, words)
	words_occurance = {}
	for word in names:
		if word in words_occurance:
			words_occurance[word] += 1
		else:
			words_occurance[word] = 1
	return words_occurance


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


def text_to_words(text):
	'''convert text to separate words

	text -> [string]
	'''
	return text.split()


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
				connections[key] = count_tokens_within_distance(positions1, positions2, dist)
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
