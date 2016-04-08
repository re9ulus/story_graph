def load_text_from_file(path_to_file):
	'''read text from file

	string -> string
	'''
	with open(path_to_file, 'r') as book:
		result = book.read()
	return result


def save_text_to_file(path_to_file, text):
	'''write text to file

	string, string -> None
	'''
	with open(path_to_file, 'w+') as f:
		f.write(text)


def load_names_from_file(path_to_file):
	'''read (name, frequency) records from file

	string -> [(string, int)]
	'''
	with open(path_to_file, 'r') as f:
		names = []
		for line in f:
			line = line.strip()
			if not line:
				break
			name, frequency = line.split(':')
			name = name.strip()
			frequency = int(frequency.strip())
			names.append((name, frequency))
		return names


def save_names_to_file(path_to_file, names):
	'''write (name, frequency) records to file

	[(string, int)] -> None
	'''
	with open(path_to_file, 'w+') as f:
		for record in names:
			f.write('{0} : {1}\n'.format(record[0], record[1]))
