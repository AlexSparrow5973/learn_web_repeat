from bs4 import BeautifulSoup
import requests


def get_html(url):
    """Функция преобразует html в string"""
    try:
        result = requests.get(url)
        result.raise_for_status()  # проверка статуса соединения, выдает exception если будут ошибки
        return result.text
    except(requests.RequestException, ValueError):
        print("Сетевая ошибка")
        return False

def get_python_news():
    html = get_html("https://www.python.org/blogs")
    if html:
        soup = BeautifulSoup(html, "html.parser")
        all_news = soup.find('ul', class_='list-recent-posts').findAll('li')  # получаем список новостей по разделителю тега 'li'
        news_list = []
        for news in all_news:
            title = news.find('a').text
            url = news.find('a')['href']
            published = news.find('time').text
            news_list.append({
                "title": title,
                "url": url,
                "published": published,
            })  # список словарей с новостями
        return news_list
    return False

        # with open("python.news.html", "w", encoding="utf-8") as f:
        #     f.write(html)

