import unittest
import book_ops


class TestBookOps(unittest.TestCase):

	def test_get_all_token_positions1(self):
		text = ['one', 'two', 'three', 'three', 'two', 'one']
		self.assertEqual(book_ops.get_all_token_positions(text, 'two'), [1, 4])

	def test_get_all_token_positions2(self):
		self.assertEqual(book_ops.get_all_token_positions([], 'test'), [])

	def test_count_token_occurrence1(self):
		text = ['one', 'two', 'three', 'three', 'two', 'one']
		self.assertEqual(book_ops.count_token_occurrence(text, 'two'), 2)

	def test_count_token_occurrence2(self):
		self.assertEqual(book_ops.count_token_occurrence([], 'test'), 0)

	def test_text_to_words1(self):
		text = 'one two three three two one'
		self.assertEqual(book_ops.text_to_words(text), ['one', 'two', 'three', 'three', 'two', 'one'])

	def test_text_to_words(self):
		text = ''
		self.assertEqual(book_ops.text_to_words(text), [])

	def test_remove_punctuation_from_text1(self):
		text = 'This, is simple text! With... some... punctuation; Maybe?'
		self.assertEqual(book_ops.remove_punctuation_from_text(text), 'This is simple text With some punctuation Maybe')

	def test_remove_punctuation_from_words1(self):
		words = 'This, is simple text! With... some... punctuation; Maybe?'.split()
		self.assertEqual(book_ops.remove_punctuation_from_words(words),  ['This', 'is', 'simple', 'text', 'With', 'some', 'punctuation', 'Maybe'])

	def test_get_names_from_words(self):
		words = 'Sam and Arya were on Naboo planet with Padme Naboo is nice planet '.split()
		self.assertEqual(book_ops.get_names_from_words(words),  {'Naboo': 2, 'Padme': 1, 'Arya': 1, 'Sam': 1})

	def test_get_names_from_text1(self):
		words = 'Sam and Arya were on Naboo planet with Padme Naboo is nice planet. I think Sam shoud be here too.'
		self.assertEqual(book_ops.get_names_from_text(words),  {'Naboo': 2, 'Padme': 1, 'Arya': 1, 'Sam': 2})

	def test_get_names_from_text2(self):
		# Sam is excluded, becouse occured only once, and in the begin of the sentence. It's Ok.
		words = 'Sam and Arya were on Naboo planet with Padme Naboo is nice planet'
		self.assertEqual(book_ops.get_names_from_text(words),  {'Naboo': 2, 'Padme': 1, 'Arya': 1})

	def test_get_names_from_text3(self):
		words = 'Here is the sentences, Harry. I think you Harry and Padme should test it. Padme is here too.'
		self.assertEqual(book_ops.get_names_from_text(words),  {'Harry': 2, 'Padme': 2})

	def test_count_tokens_within_distance1(self):
		pos1_list = [0, 3, 5 , 9]
		pos2_list = [1, 4]
		dist = 0
		self.assertEqual(book_ops.count_tokens_within_distance(pos1_list, pos2_list, dist), 0)

	def test_count_tokens_within_distance2(self):
		pos1_list = [0, 3, 5 , 9]
		pos2_list = [1, 8]
		dist = 1
		self.assertEqual(book_ops.count_tokens_within_distance(pos1_list, pos2_list, dist), 2)

	def test_count_tokens_within_distance3(self):
		pos1_list = [0, 3, 5 , 9]
		pos2_list = [3]
		dist = 0
		self.assertEqual(book_ops.count_tokens_within_distance(pos1_list, pos2_list, dist), 1)

	def test_count_tokens_within_distance4(self):
		pos1_list = [0, 3, 5 , 9]
		pos2_list = [1, 4]
		dist = 1
		self.assertEqual(book_ops.count_tokens_within_distance(pos1_list, pos2_list, dist), 3)

	def test_count_tokens_within_distance5(self):
		pos1_list = []
		pos2_list = [1, 4]
		dist = 1
		self.assertEqual(book_ops.count_tokens_within_distance(pos1_list, pos2_list, dist), 0)

	def test_count_tokens_within_distance6(self):
		pos1_list = [0, 3, 5 , 9]
		pos2_list = []
		dist = 1
		self.assertEqual(book_ops.count_tokens_within_distance(pos1_list, pos2_list, dist), 0)

	def test_get_connection_powers1(self):
		records = {'Arya': [1, 3, 5],
					'Black': [2],
					'Luke': [6, 7],
					'Frodo': [4, 8]}
		expected = {('Arya', 'Frodo'): 2, ('Frodo', 'Luke'): 1, ('Arya', 'Luke'): 1,
					('Arya', 'Black'): 2}
		self.assertEqual(book_ops.get_connection_powers(records, 1), expected)

	def test_get_connections1(self):
		records = {'Arya': [1, 3, 5],
					'Black': [2],
					'Luke': [6, 7],
					'Frodo': [4, 8]}
		expected = [('Arya', 'Black'), ('Arya', 'Frodo'), ('Arya', 'Luke'), ('Frodo', 'Luke')]
		self.assertEqual(sorted(book_ops.get_connections(records, 1)), expected)


if __name__ == '__main__':
	unittest.main()
