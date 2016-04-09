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

	def test_get_names(self):
		words = 'Sam and Arya were on Naboo planet with Padme Naboo is nice planet '.split()
		self.assertEqual(book_ops.get_names(words),  [('Naboo', 2), ('Padme', 1), ('Arya', 1), ('Sam', 1)])

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


if __name__ == '__main__':
	unittest.main()
