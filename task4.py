from bs4 import BeautifulSoup
from task2 import filter_text, lemmatize
import numpy as np


def load_data(k):
    terms = {}

    for i in range(1, k + 1):
        with open('movies/' + str(i) + '.html', encoding="utf-8") as f:
            content = f.read()

            soup = BeautifulSoup(content, features="html.parser")

            for script in soup(["script", "style"]):
                script.extract()

            text = soup.get_text()
            lines = (line.strip() for line in text.splitlines())
            chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
            text = '\n'.join(chunk for chunk in chunks if chunk)
            text = filter_text(text)

            terms[i] = text.split(' ')

    return terms


def calculate_idf(word, terms):
    count = 0
    for term_list in terms.values():
        if word in term_list:
            count += 1
    idf = np.log10(len(terms) / count)
    return idf


def calculate_and_write_tf_idf(terms, path):
    for i, term_list in terms.items():
        result_text = ''
        unique_terms = set(term_list)
        if '' in unique_terms:
            unique_terms.remove('')

        for word in unique_terms:
            word_count = len([x for x in term_list if x == word])
            tf = word_count / len(unique_terms)
            idf = calculate_idf(word, terms)
            tf_idf = round(tf * idf, 15)

            result_text += word + ' ' + str(idf) + ' ' + str(tf_idf) + '\n'

        with open(path + str(i) + '.txt', "w", encoding="utf-8") as f:
            f.write(result_text)


def run_for_terms():
    k = 100
    terms = load_data(k)

    calculate_and_write_tf_idf(terms, 'tf-idf/terms/')


def run_for_lemmas():
    k = 100
    terms = load_data(k)
    terms = lemmatize_terms(terms)

    calculate_and_write_tf_idf(terms, 'tf-idf/lemmas/')


def lemmatize_terms(terms):
    lem_terms = {}
    for i, term_list in terms.items():
        lem_terms[i] = [lemmatize(x) for x in term_list]
    return lem_terms


if __name__ == '__main__':
    run_for_terms()
    run_for_lemmas()
