def save_text_to_file(path_to_file, text):
    """write text to file

    string, string -> None
    """
    with open(path_to_file, 'w+') as f:
        f.write(text)


def load_text_from_file(path_to_file):
    """read text from file

    string -> string
    """
    with open(path_to_file, 'r') as book:
        result = book.read()
    return result


def save_names_to_file(names, path_to_file):
    """write {name: occurance} dict to file

    string, {string: int} -> None
    """
    with open(path_to_file, 'w+') as f:
        for name, count in sorted(names.items(), key=lambda item: item[1], reverse=True):
            f.write('{0} : {1}\n'.format(name, count))


def load_names_from_file(path_to_file):
    """read {name: occurance} records from file

    string -> {string: int}
    """
    names = {}
    with open(path_to_file, 'r') as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            name, occurance = line.split(':')
            name = name.strip()
            occurance = int(occurance.strip())
            names[name] = occurance
    return names


def save_token_positions_to_file(path_to_file, positions):
    """write {token: [positions]} dict to file

    string, {string: [int]} -> None
    """
    with open(path_to_file, 'w+') as f:
        for token, positions in sorted(positions.items(), key=lambda item: len(item[1]), reverse=True):
            f.write('{0} : {1}\n'.format(token, ' '.join(map(str, positions))))


def load_token_positions_from_file(path_to_file):
    """load {token: [positions]} dict from file

    string -> {string: [int]}
    """
    tokens = {}
    with open(path_to_file, 'r') as f:
        for line in f:
            line = line.strip()
            if not line:
                break
            name, positions = line.split(':')
            name = name.strip()
            positions = list(map(lambda item: int(item.strip()), positions.split()))
            tokens[name] = positions
    return tokens
