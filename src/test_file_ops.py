import unittest
import file_ops


TEST_FILES_FOLDER = './files_for_tests/'


class TestBookOps(unittest.TestCase):

    def test_load_text_from_file1(self):
        path_to_file = TEST_FILES_FOLDER + 'test_text1.txt'
        expected_text = 'Test header.\n\nSome linese of text.\nAnd another one.\n\nAnd here comes the third.'
        self.assertEqual(file_ops.load_text_from_file(path_to_file), expected_text)

    def test_save_text_to_file1(self):
        path_to_file = TEST_FILES_FOLDER + 'test_write_text1.txt'
        expected_text = 'Test header.\n\nSome linese of text.\nAnd another one.\n\nAnd here comes the third.'
        open(path_to_file, 'w+').close()
        file_ops.save_text_to_file(path_to_file, expected_text)
        self.assertEqual(file_ops.load_text_from_file(path_to_file), expected_text)

    def test_load_names_from_file1(self):
        path_to_file = TEST_FILES_FOLDER + 'test_names1.txt'
        names = {'Arya': 3, 'Luke': 8, 'Harry': 4}
        self.assertEqual(file_ops.load_names_from_file(path_to_file), names)

    def test_save_names_to_file1(self):
        path_to_file = TEST_FILES_FOLDER + 'test_write_names1.txt'
        names = {'Arya': 3, 'Luke': 8, 'Harry': 4}
        open(path_to_file, 'w+').close()
        file_ops.save_names_to_file(path_to_file, names)
        self.assertEqual(file_ops.load_names_from_file(path_to_file), names)

    def test_load_token_positions_from_file1(self):
        path_to_file = TEST_FILES_FOLDER + 'test_positions1.txt'
        positions = {'Arya': [4, 7, 9], 'Luke': [88, 14, 5], 'Harry': [9]}
        self.assertEqual(file_ops.load_token_positions_from_file(path_to_file), positions)

    def test_save_token_positions_to_file1(self):
        path_to_file = TEST_FILES_FOLDER + 'test_write_positions1.txt'
        positions = {'Arya': [4, 7, 9], 'Luke': [88, 14, 5], 'Harry': [9]}
        open(path_to_file, 'w+').close()
        file_ops.save_token_positions_to_file(path_to_file, positions)
        self.assertEqual(file_ops.load_token_positions_from_file(path_to_file), positions)


if __name__ == '__main__':
    unittest.main()
