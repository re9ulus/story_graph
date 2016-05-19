import book_ops
import file_ops

# TODO: 
# 1. Stemming/lemmatization of the file (for names may be unnecessary, becouse they are unchanged)
# 2. Find all words that start with capital later, when previous letter wasn't in '.!?' (sentance end)
# 3. Remove all non ascii characters from book
# 4. Think about functions that accepts already splitted text, to avoid splitting in evety function
#


# Trying to get words that are not the beginning of the sentance
def get_names_v2():
    """(name, frequency) sorted by frequency

    text -> [(string, int)]
    """
    for word in words:
        if word in words_occurance:
            words_occurance[word] += 1
        else:
            words_occurance[word] = 1
    words_occurance = zip(words_occurance.keys(), words_occurance.values())
    words_occurance = sorted(words_occurance, key=lambda item: item[1], reverse=True)
    return words_occurance


if __name__ == '__main__':
    prepared_book_path = 'test_result.txt'

    raw_text = file_ops.load_text_from_file('../books/storm_of_swords.txt')
    book_text = book_ops.remove_punctuation_from_text(raw_text)
    words = book_ops.text_to_words(book_text)

    with open(prepared_book_path, 'w+') as f:
        f.write(book_text)
    words_occurance = book_ops.get_names(words)
    with open('get_names.txt', 'w+') as f:
        for occurance in words_occurance:
            f.write('{0} : {1}\n'.format(occurance[0], occurance[1]))
