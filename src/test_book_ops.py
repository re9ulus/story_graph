import unittest
import book_ops


class TestBookOps(unittest.TestCase):

	def test_get_all_token_positions1(self):
		text = 'one two three three two one'
		self.assertEqual(book_ops.get_all_token_positions(text, 'two'), [1, 4])

	def test_get_all_token_positions2(self):
		self.assertEqual(book_ops.get_all_token_positions('', 'test'), [])

	def test_count_token_occurrence1(self):
		text = 'one two three three two one'
		self.assertEqual(book_ops.count_token_occurrence(text, 'two'), 2)

	def test_count_token_occurrence2(self):
		self.assertEqual(book_ops.count_token_occurrence('', 'test'), 0)

	def test_text_to_words(self):
		text = 'one two three three two one'
		self.assertEqual(book_ops.text_to_words(text), ['one', 'two', 'three', 'three', 'two', 'one'])

	def test_text_to_words(self):
		text = ''
		self.assertEqual(book_ops.text_to_words(text), [])

if __name__ == '__main__':
	unittest.main()
