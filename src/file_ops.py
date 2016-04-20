def save_text_to_file(path_to_file, text):
	'''write text to file

	string, string -> None
	'''
	with open(path_to_file, 'w+') as f:
		f.write(text)


def load_text_from_file(path_to_file):
	'''read text from file

	string -> string
	'''
	with open(path_to_file, 'r') as book:
		result = book.read()
	return result


def save_names_to_file(path_to_file, names):
	'''write (name, frequency) records to file

	string, {string: int} -> None
	'''
	with open(path_to_file, 'w+') as f:
		for name, count in names.iteritems():
			f.write('{0} : {1}\n'.format(name, count))


def load_names_from_file(path_to_file):
	'''read (name, frequency) records from file

	string -> {string: int}
	'''
	names = {}
	with open(path_to_file, 'r') as f:
		for line in f:
			line = line.strip()
			if not line:
				break
			name, frequency = line.split(':')
			name = name.strip()
			frequency = int(frequency.strip())
			names[name] = frequency
	return names


def save_token_positions_to_file(path_to_file, positions):
	'''write (token, [positions]) records to file

	string [(string, [int])] -> None
	'''
	with open(path_to_file, 'w+') as f:
		for record in positions:
			f.write('{0} : {1}\n'.format(record[0], ' '.join(map(str, record[1]))))


def load_token_positions_from_file(path_to_file):
	'''load (token, [positions]) records from file

	string -> [(string, [int])]
	'''
	names = []
	with open(path_to_file, 'r') as f:
		for line in f:
			line = line.strip()
			if not line:
				break
			name, positions = line.split(':')
			name = name.strip()
			positions = map(lambda item: int(item.strip()), positions.split())
			names.append((name, positions))
	return names

