import requests
from bs4 import BeautifulSoup


def run():
    url = "https://www.kinoafisha.info/rating/movies/"
    response = requests.get(url)

    soup = BeautifulSoup(response.content, 'lxml')

    movies = soup.find('div', {'class': 'ratings_list'}).find_all('div', {'class': 'movieList_item'})
    index = ''

    num = 0
    for movie in movies:
        num += 1
        url = movie.find('a')['href']

        movie_page = requests.get(url)
        with open('movies/' + str(num) + '.html', "w", encoding="utf-8") as f:
            f.write(movie_page.text)

        index += str(num) + ' ' + url + '\n'

        print(str(num) + '/100')

    with open('index.txt', "w", encoding="utf-8") as f:
        f.write(index)


if __name__ == '__main__':
    run()
