import operator
from decimal import Decimal

from numpy import dot
from numpy.linalg import norm

from task2 import lemmatize


def read_movie_vectors():
    result = {}

    k = 100
    for i in range(1, k + 1):
        with open('tf-idf/lemmas/' + str(i) + '.txt', encoding="utf-8") as f:
            result[i] = f.readlines()

    return result

def calc_cos_similarity(tf_idf_vector, tf_idf_movie_vector):
    query_vector = list(tf_idf_vector.values())
    movie_vector = list(tf_idf_movie_vector.values())

    if norm(query_vector) == 0 or norm(movie_vector) == 0:
        return 0

    return dot(query_vector, movie_vector) / (norm(query_vector) * norm(movie_vector))
    # num = decimal_dot_product(query_vector, movie_vector)
    # den = Decimal(norm(query_vector) * norm(movie_vector))
    # return num / den


def decimal_dot_product(list1, list2):
    result = Decimal(0)
    for i in range(0, len(list1)):
        result += Decimal(list1[i]) * Decimal(list2[i])
    return result


def search(query):
    query_terms = [lemmatize(x) for x in query.split()]
    unique_terms = set(query_terms)

    tf_vector = {}
    for term in unique_terms:
        word_count = len([x for x in query_terms if x == term])
        tf = word_count / len(query_terms)
        tf_vector[term] = tf

    movie_vectors = read_movie_vectors()

    cos_sim_result = {}

    for i, lines in movie_vectors.items():
        tf_idf_vector = {}
        tf_idf_movie_vector = {}
        movie_terms = []

        for line in lines:
            line_data = line.split()
            term = line_data[0]
            idf = line_data[1]
            tf_idf = line_data[2]

            if term in unique_terms:
                movie_terms.append(term)
                tf_idf_vector[term] = tf_vector[term] * float(idf)
                tf_idf_movie_vector[term] = float(tf_idf)

        for term in unique_terms:
            if term not in movie_terms:
                tf_idf_vector[term] = 1
                tf_idf_movie_vector[term] = 0

        cos_sim = calc_cos_similarity(tf_idf_vector, tf_idf_movie_vector)
        if cos_sim != 0:
            cos_sim_result[i] = cos_sim
            # print(tf_idf_vector.values())
            # print(tf_idf_movie_vector.values())
            # print()

    sorted_result = sorted(cos_sim_result.items(), key=operator.itemgetter(1), reverse=True)
    result = dict(sorted_result)
    return result
    # return list(result.keys())


def run():
    query1 = 'в городе происходит ряд дерзких разбойных нападений'
    query2 = 'Геннадий Петрович Козодоев, злостный мошенник и контрабандист'

    search_result = search(query1)
    for i, cos_sim in search_result.items():
        print('Документ ' + str(i) + '.html. Сходимость: ' + str(cos_sim))


if __name__ == '__main__':
    run()
