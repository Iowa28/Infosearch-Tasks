from task2 import tokenize, lemmatize


def get_lemmas():
    lemmas = []

    with open('lemmas.txt', encoding="utf-8") as f:
        lines = f.readlines()

        for line in lines:
            lemma = line.split(':')[0]
            lemmas.append(lemma)

    return lemmas


def get_inverted_index(lemmas):
    inverted_index = {}

    for lemma in lemmas:
        inverted_index[lemma] = []

    n = 100

    for i in range(1, n + 1):
        with open('movies/' + str(i) + '.html', encoding="utf-8") as f:
            content = f.read()

            # метод из файла task2
            tokens = tokenize(content)

            for token in tokens:
                # метод из файла task2
                token_lemma = lemmatize(token)

                if lemmas.count(token_lemma) > 0 and inverted_index.get(token_lemma).count(i) == 0:
                    inverted_index.get(token_lemma).append(i)

        print(str(i) + '/100')

    return inverted_index


def make_inverted_index():
    lemmas = get_lemmas()

    inverted_index = get_inverted_index(lemmas)

    inverted_index_text = ''
    for lemma, indexes in inverted_index.items():
        inverted_index_text += lemma + ' '
        for index in indexes:
            inverted_index_text += str(index) + ' '
        inverted_index_text += '\n'

    with open('inverted_index.txt', "w", encoding="utf-8") as f:
        f.write(inverted_index_text)


def read_inverted_index():
    inverted_index = {}

    with open('inverted_index.txt', encoding="utf-8") as f:
        lines = f.readlines()

        for line in lines:
            lemma = line.split()[0]
            indexes = line.split()
            indexes.pop(0)

            inverted_index[lemma] = indexes

    return inverted_index


def get_links(indexes):
    links = []

    with open('index.txt', encoding="utf-8") as f:
        lines = f.readlines()

        for line in lines:
            number, link = line.split()

            if number in indexes:
                links.append(link)

    return links


def search(words_text, inverted_index):
    words_indexes = set()

    split_or = words_text.split('|')
    split_and = words_text.split('&')

    if len(split_or) > 1:
        for words_or in split_or:
            words_indexes = words_indexes.union(search(words_or, inverted_index))
    elif len(split_and) > 1:
        for i, words_and in enumerate(split_and):
            if i == 0:
                words_indexes = search(words_and, inverted_index)
            else:
                words_indexes = words_indexes.intersection(search(words_and, inverted_index))
    elif words_text[0] == '!':
        word_lemma = lemmatize(words_text[1:])
        exclude_indexes = []

        for lemma, indexes in inverted_index.items():
            if word_lemma != lemma:
                words_indexes = words_indexes.union(indexes)
            else:
                exclude_indexes = indexes

        words_indexes = words_indexes.difference(exclude_indexes)
    else:
        word_lemma = lemmatize(words_text)

        for lemma, indexes in inverted_index.items():
            if word_lemma == lemma:
                return set(indexes)

    return words_indexes


def make_search():
    inverted_index = read_inverted_index()

    words_text = 'иван'
    # words_text = 'лавочке|иван'
    # words_text = 'предполагаться&иван'
    # words_text = 'лавочке|Предполагалось&иван'
    # words_text = 'иван&!офицеры'
    # words_text = 'иван&!Васильевич'

    indexes = search(words_text, inverted_index)

    links = get_links(indexes)

    for link in links:
        print(link)


if __name__ == '__main__':
    # make_inverted_index()

    make_search()
