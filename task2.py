import re
from bs4 import BeautifulSoup
import pymorphy2


morph = pymorphy2.MorphAnalyzer()


def filter_text(text):
    return re.sub('[^а-яА-ЯёЁa-zA-Z]+', ' ', text)


def tokenize(content):
    soup = BeautifulSoup(content, features="html.parser")

    for script in soup(["script", "style"]):
        script.extract()

    text = soup.get_text()

    lines = (line.strip() for line in text.splitlines())

    chunks = (phrase.strip() for line in lines for phrase in line.split("  "))

    text = '\n'.join(chunk for chunk in chunks if chunk)

    text = filter_text(text)

    return set(text.split(' '))


def get_tokens():
    n = 100

    tokens = set()

    for i in range(1, n + 1):
        with open('movies/' + str(i) + '.html', encoding="utf-8") as f:
            content = f.read()

            content_tokens = tokenize(content)

            tokens = tokens.union(content_tokens)

    return tokens


def pos(word):
    return morph.parse(word)[0].tag.POS


def normalize_tokens(tokens):
    functors_pos = {'INTO', 'PRCL', 'CONJ', 'PREP'}
    result = list()

    for token in tokens:
        token_pos = pos(token)
        if (token_pos is not None) and (token_pos not in functors_pos):
            result.append(token)

    return result


def write_tokens(tokens):
    tokens_text = ''

    for token in tokens:
        tokens_text += token + '\n'

    with open('tokens.txt', "w", encoding="utf-8") as f:
        f.write(tokens_text)


def lemmatize(word):
    p = morph.parse(word)[0]
    return p.normal_form


def get_lemmas(tokens):
    lemmas = {}

    for token in tokens:
        lemma = lemmatize(token)
        if lemmas.get(lemma) is not None:
            lemmas.get(lemma).append(token)
        else:
            lemmas[lemma] = [token]

    return lemmas


def write_lemmas(lemmas):
    lemmas_text = ''

    for lemma, tokens in lemmas.items():
        lemmas_text += lemma + ': '
        for token in tokens:
            lemmas_text += token + ' '
        lemmas_text += '\n'

    with open('lemmas.txt', "w", encoding="utf-8") as f:
        f.write(lemmas_text)


def run():
    # получаем список токенов из html-файлов
    tokens = get_tokens()

    # удаляем предлоги и союзы
    tokens = normalize_tokens(tokens)

    # записываем токены в файл
    write_tokens(tokens)

    # разбиваем токены на леммы (ключ - лемма, значение - список токенов)
    lemmas = get_lemmas(tokens)

    # записываем леммы в файл
    write_lemmas(lemmas)


if __name__ == '__main__':
    run()
