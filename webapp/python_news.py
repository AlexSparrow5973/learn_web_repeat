from datetime import datetime
from bs4 import BeautifulSoup
import requests

from webapp.db import db
from webapp.news.models import News


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
            published = news.find('time')['datetime']
            try:
                published = datetime.strptime(published, '%Y-%m-%d')
            except ValueError:
                published = datetime.now()
            save_news(title, url, published)

def save_news(title, url, published):
    news_exists = News.query.filter(News.url==url)
    if not news_exists:
        news_news = News(title=title, url=url, published=published)
        db.session.add(news_news)
        db.session.commit()
