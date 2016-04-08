import unittest
import file_ops


TEST_FILES_FOLDER = './files_for_tests/'


class TestBookOps(unittest.TestCase):

	def test_get_text_from_file1(self):
		path_to_file = TEST_FILES_FOLDER + 'test_text1.txt'
		expected_text = 'Test header.\n\nSome linese of text.\nAnd another one.\n\nAnd here comes the third.'
		self.assertEqual(file_ops.get_text_from_file(path_to_file), expected_text)


if __name__ == '__main__':
	unittest.main()
