import re
import math
import string
from collections import Counter
from nltk.stem.snowball import SnowballStemmer

# TODO: Add tests for stemming function
# TODO: Add full pipeline to BookOps class

# TODO: Maybe add name_occurances to this class ?

class BookOps:

	stemmer = SnowballStemmer('english')

	def __init__(self, text='', distance=6, min_occurance=0, use_stemmer=False):
		self._raw_text = text
		self._text = self.remove_punctuation_from_text(self._raw_text)
		self._use_stemmer = use_stemmer
		self._min_occurance = min_occurance

		self._name_pattern = '\w[^\.\!\?\"]\s+([A-Z][a-z]+)'

		self._words = self.text_to_words(self._text)
		self._stemmed_words = self.stem_words(self._words)

		self._names = []


	@classmethod
	def is_capitalized(cls, word):
		return len(word) and word[0].isupper()


	@classmethod
	def text_to_words(cls, text):
		'''convert text to separate words

		string -> [string]
		'''
		return text.split()

	@classmethod
	def remove_punctuation_from_text(cls, text):
		'''remove punctuation from text

		string -> string
		remove all puncutation
		'''
		exclude = set(string.punctuation)
		return ''.join(ch for ch in text if ch not in exclude)

	@classmethod
	def remove_punctuation_from_words(cls, words):
		'''remove punctuation from each word

		[string] -> string
		remove all puncutation
		'''
		return list(map(cls.remove_punctuation_from_text, words))


	def stem_string(text):
		'''stem text

		string -> string
		'''
		return stemmer.stem(text)

	@classmethod
	def get_stem_words_dict(cls, names):
		'''get dict of stemmed words to original words

		[string] -> {string: string}
		'''
		stemmed_words = {}
		for name in names:
			stemmed = cls.stemmer.stem(name)
			# based on the assumption that the first occurrence of the name will be without 's' at the end. Don't change
			if stemmed not in stemmed_words:
				stemmed_words[stemmed] = name
		return stemmed_words

	@classmethod
	def stem_words(cls, words):
		'''stem list of words

		[string] -> [string]
		'''
		return map(cls.stemmer.stem, words)

	def get_names_from_words(self):
		'''get dict of names from words

		[string] -> {string: int}
		name - is capitaliazed word.
		dict key is name
		dict value is number of occurances of the name in text
		'''
		# TODO: Add "use stemmer to this function"
		names = filter(self.is_capitalized, self._words)
		words_occurance = Counter(names)
		if self._min_occurance > 0:
			words_occurance = {k: v for k, v in words_occurance.iteritems() if v > self._min_occurance}
		return words_occurance

	def get_names_from_text(self):
		'''get dict of names in the text

		{string: int}
		name - is capitaliazed word.
		dict key is name
		dict value is number of occurances of the name in text
		'''
		names = set(re.findall(self._name_pattern, self._raw_text))
		words = filter(self.is_capitalized, self._words)

		if self._use_stemmer:
			stem_words_dict = self.get_stem_words_dict(names)
			names = self.stem_words(names)
			words = self._stemmed_words #stem_words(words)

		words_occurance = Counter()
		for word in words:
			if word in names:
				words_occurance[word] += 1

		if self._use_stemmer:
			words_occurance = {stem_words_dict[name]: words_occurance[name] for name in names}

		if self._min_occurance > 0:
			words_occurance = {k: v for k, v in words_occurance.iteritems() if v > self._min_occurance}

		return words_occurance


	def name_positions(self, name):
		'''get all positions of the name in the string array

		string -> [int]
		'''
		words = self._words
		if self._use_stemmer:
			words = self._stemmed_words
			name = self.stemmer.stem(name)
		return [i for i, word in enumerate(words) if word == name]


	def all_names_positions(self):
		'''get positions for every name in names

		 -> {string: [int]}
		'''
		return {name: self.name_positions(name) for name in self.get_names()}


	def count_token_occurrence(self, token):
		'''find number of occurances of the token in the words of book

		string -> int
		'''
		return self._words.count(token)


	@classmethod
	def count_tokens_within_distance(cls, token1_pos, token2_pos, dist):
		'''count number of occurrences token1 within distance to token2

		[int], [int], dist -> int
		'''
		score = 0
		for i in token1_pos:
			for j in token2_pos:
				if abs(i - j) <= dist:
					score += 1
				elif j > i and abs(i - j) > dist:
					break
		return score


	@classmethod
	def get_connection_powers(cls, name_occurances, dist):
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
					conn_power = cls.count_tokens_within_distance(positions1, positions2, dist)
					if conn_power > 0:
						connections[key] = conn_power
		return connections


	@classmethod
	def get_connections(cls, name_occurances, dist):
		'''get connections from {name: [positions]} dict

		{string: [int]}, int -> [(string, string)]
		'''
		connections = []
		connection_powers = cls.get_connection_powers(name_occurances, dist)
		for connection, power in connection_powers.iteritems():
			if power > 0:
				connections.append(connection)
		return connections


	def get_words_near_position(self, index, delta):
		'''get words from text[index-delta:index+delta]

		int, int -> [string]
		'''
		min_index = index - delta
		min_index = 0 if min_index < 0 else min_index
		max_index = index + delta
		max_index = len(self._words) if max_index > len(self._words) else max_index
		return self._words[min_index:max_index]


	def get_all_positions_surroundings(self, name_occurances, delta):
		'''get all surrounding from text for each position in name_occurances
		
		[int], int -> [[string]]
		'''
		res_surroundings = []
		for occurance_ind in name_occurances:
			res_surroundings.append(self.get_words_near_position(occurance_ind, delta))
		return res_surroundings


	def get_all_connection_positions(self, name1, name2, dist):
		'''get positions of connections between 2 characters in the book

		string, string, dist -> [int]
		'''
		positions = []
		name_pos1 = self.name_positions(name1)
		name_pos2 = self.name_positions(name2)
		for i in name_pos1:
			for j in name_pos2:
				if abs(i - j) <= dist:
					positions.append((i + j) / 2)
				elif j > i and abs(i - j) > dist:
					break
		return positions


	def set_names(self, names):
		self._names = names


	def get_names(self):
		return self._names
