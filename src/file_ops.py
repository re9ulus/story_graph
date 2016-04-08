def get_text_from_file(path_to_file):
	'''read text from file

	string -> string
	'''
	with open(path_to_file, 'r') as book:
		result = book.read()
	return result
