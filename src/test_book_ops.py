import unittest
from book_ops import BookOps


class TestBookOps(unittest.TestCase):

	def test_name_positions1(self):
		b = BookOps(text='')
		b._words = ['one', 'two', 'three', 'three', 'two', 'one']
		self.assertEqual(b.name_positions('two'), [1, 4])

	def test_name_positions2(self):
		b = BookOps(text='')
		self.assertEqual(b.name_positions('test'), [])

	def test_all_names_positions1(self):
		b = BookOps(text='')
		b.set_names(['test1', 'test2'])
		self.assertEqual(b.all_names_positions(), {'test1': [], 'test2': []})

	def test_all_names_positions2(self):
		b = BookOps(text='')
		b._words = ['one', 'two', 'three', 'three', 'two', 'one']
		self.assertEqual(b.all_names_positions(), {})

	def test_all_names_positions3(self):
		b = BookOps(text='')
		b._words = ['one', 'two', 'three', 'three', 'two', 'one']
		b.set_names(['three', 'two'])
		self.assertEqual(b.all_names_positions(), {'three': [2, 3], 'two': [1, 4]})

	def test_count_token_occurrence1(self):
		b = BookOps(text='')
		b._words = ['one', 'two', 'three', 'three', 'two', 'one']
		self.assertEqual(b.count_token_occurrence('two'), 2)

	def test_count_token_occurrence2(self):
		b = BookOps(text='')
		self.assertEqual(b.count_token_occurrence('test'), 0)

	def test_text_to_words1(self):
		b = BookOps(text='')
		text = 'one two three three two one'
		self.assertEqual(b.text_to_words(text), ['one', 'two', 'three', 'three', 'two', 'one'])

	def test_text_to_words2(self):
		b = BookOps(text='')
		text = ''
		self.assertEqual(b.text_to_words(text), [])

	def test_remove_punctuation_from_text1(self):
		b = BookOps(text='')
		text = 'This, is simple text! With... some... punctuation; Maybe?'
		self.assertEqual(b.remove_punctuation_from_text(text), 'This is simple text With some punctuation Maybe')

	def test_remove_punctuation_from_words1(self):
		b = BookOps(text='')
		words = 'This, is simple text! With... some... punctuation; Maybe?'.split()
		self.assertEqual(b.remove_punctuation_from_words(words),  ['This', 'is', 'simple', 'text', 'With', 'some', 'punctuation', 'Maybe'])

	def test_get_names_from_words(self):
		b = BookOps(text='Sam and Arya were on Naboo planet with Padme Naboo is nice planet')
		self.assertEqual(b.get_names_from_words(),  {'Naboo': 2, 'Padme': 1, 'Arya': 1, 'Sam': 1})

	# TODO: Add test with use_stemmer=True
	def test_get_names_from_text1(self):
		b = BookOps(text='Sam and Arya were on Naboo planet with Padme Naboo is nice planet. I think Sam shoud be here too.', use_stemmer=False)
		self.assertEqual(b.get_names_from_text(),  {'Naboo': 2, 'Padme': 1, 'Arya': 1, 'Sam': 2})

	def test_get_names_from_text2(self):
		# Sam is excluded, becouse occured only once, and in the begin of the sentence. It's Ok.
		b = BookOps(text='Sam and Arya were on Naboo planet with Padme Naboo is nice planet', use_stemmer=False)
		self.assertEqual(b.get_names_from_text(),  {'Naboo': 2, 'Padme': 1, 'Arya': 1})

	def test_get_names_from_text3(self):
		b = BookOps(text='Here is the sentences, Harry. I think you Harry and Padme should test it. Padme is here too.', use_stemmer=False)
		self.assertEqual(b.get_names_from_text(),  {'Harry': 2, 'Padme': 2})

	def test_count_tokens_within_distance1(self):
		b = BookOps(text='')
		pos1_list = [0, 3, 5 , 9]
		pos2_list = [1, 4]
		dist = 0
		self.assertEqual(b.count_tokens_within_distance(pos1_list, pos2_list, dist), 0)

	def test_count_tokens_within_distance2(self):
		b = BookOps(text='')
		pos1_list = [0, 3, 5 , 9]
		pos2_list = [1, 8]
		dist = 1
		self.assertEqual(b.count_tokens_within_distance(pos1_list, pos2_list, dist), 2)

	def test_count_tokens_within_distance3(self):
		b = BookOps(text='')
		pos1_list = [0, 3, 5 , 9]
		pos2_list = [3]
		dist = 0
		self.assertEqual(b.count_tokens_within_distance(pos1_list, pos2_list, dist), 1)

	def test_count_tokens_within_distance4(self):
		b = BookOps(text='')
		pos1_list = [0, 3, 5 , 9]
		pos2_list = [1, 4]
		dist = 1
		self.assertEqual(b.count_tokens_within_distance(pos1_list, pos2_list, dist), 3)

	def test_count_tokens_within_distance5(self):
		b = BookOps(text='')
		pos1_list = []
		pos2_list = [1, 4]
		dist = 1
		self.assertEqual(b.count_tokens_within_distance(pos1_list, pos2_list, dist), 0)

	def test_count_tokens_within_distance6(self):
		b = BookOps(text='')
		pos1_list = [0, 3, 5 , 9]
		pos2_list = []
		dist = 1
		self.assertEqual(b.count_tokens_within_distance(pos1_list, pos2_list, dist), 0)

	def test_get_connection_powers1(self):
		b = BookOps(text='')
		records = {'Arya': [1, 3, 5],
					'Black': [2],
					'Luke': [6, 7],
					'Frodo': [4, 8]}
		expected = {('Arya', 'Frodo'): 2, ('Frodo', 'Luke'): 1, ('Arya', 'Luke'): 1,
					('Arya', 'Black'): 2}
		self.assertEqual(b.get_connection_powers(records, 1), expected)

	def test_get_connections1(self):
		b = BookOps(text='')
		records = {'Arya': [1, 3, 5],
					'Black': [2],
					'Luke': [6, 7],
					'Frodo': [4, 8]}
		expected = [('Arya', 'Black'), ('Arya', 'Frodo'), ('Arya', 'Luke'), ('Frodo', 'Luke')]
		self.assertEqual(sorted(b.get_connections(records, 1)), expected)

	def test_get_words_near_position1(self):
		b = BookOps(text='')
		self.assertEqual(sorted(b.get_words_near_position(0, 5)), [])

	def test_get_words_near_position2(self):
		b = BookOps(text='Sam and Arya were on Naboo planet with Padme Naboo is nice planet')
		self.assertEqual(b.get_words_near_position(5, 4), ['and', 'Arya', 'were', 'on', 'Naboo', 'planet', 'with', 'Padme'])

	def test_get_words_near_position3(self):
		b = BookOps(text='Sam and Arya were on Naboo planet with Padme Naboo is nice planet')
		self.assertEqual(b.get_words_near_position(2, 4), ['Sam', 'and', 'Arya', 'were', 'on', 'Naboo'])

	def test_get_words_near_position4(self):
		b = BookOps(text='Sam and Arya were on Naboo planet with Padme Naboo is nice planet')
		self.assertEqual(b.get_words_near_position(10, 4), ['planet', 'with', 'Padme', 'Naboo', 'is', 'nice', 'planet'])

	def test_get_all_connection_positions1(self):
		b = BookOps(text='Sam and Arya were on Naboo planet with Padme Naboo is nice planet')
		self.assertEqual(b.get_all_connection_positions('Sam', 'Arya', 3), [1])

	def test_get_all_connection_positions2(self):
		b = BookOps(text='Sam and Arya were on Naboo planet with Padme Naboo is nice planet')
		self.assertEqual(b.get_all_connection_positions('Sam', 'Padme', 3), [])

	def test_get_all_connection_positions3(self):
		b = BookOps(text='Sam and Arya were on Naboo planet with Padme Naboo is nice planet')
		self.assertEqual(b.get_all_connection_positions('Padme', 'Naboo', 3), [6, 8])

	def test_get_all_connection_positions4(self):
		b = BookOps(text='')
		self.assertEqual(b.get_all_connection_positions('Padme', 'Naboo', 3), [])

	def test_set_names1(self):
		b = BookOps(text='')
		self.assertEqual(b._names, [])
		b.set_names(['Padme', 'Frodo'])
		self.assertEqual(b._names, ['Padme', 'Frodo'])

	def test_get_names1(self):
		b = BookOps(text='')
		self.assertEqual(b.get_names(), [])
		b._names = ['Padme', 'Frodo']
		self.assertEqual(b.get_names(), ['Padme', 'Frodo'])

if __name__ == '__main__':
	unittest.main()
