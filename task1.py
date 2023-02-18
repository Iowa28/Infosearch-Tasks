import requests
from bs4 import BeautifulSoup


def run():
    # адрес сайта с фильмами
    url = "https://www.kinoafisha.info/rating/movies/"
    response = requests.get(url)

    soup = BeautifulSoup(response.content, 'lxml')

    # поиск нужного элемента с ссылками на фильмы
    movies = soup.find('div', {'class': 'ratings_list'}).find_all('div', {'class': 'movieList_item'})
    index = ''

    num = 0
    for movie in movies:
        # извеление url, который ведет на страницу фильма
        url = movie.find('a')['href']
        num += 1

        # скачивание страницы и сохранение
        movie_page = requests.get(url)
        with open('movies/' + str(num) + '.html', "w", encoding="utf-8") as f:
            f.write(movie_page.text)

        index += str(num) + ' ' + url + '\n'

        print(str(num) + '/100')

    # сохранение списка ссылок в отдельный файл
    with open('index.txt', "w", encoding="utf-8") as f:
        f.write(index)


if __name__ == '__main__':
    run()
