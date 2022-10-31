import requests

from webapp.db import db
from webapp.news.models import News


def get_html(url):
    """Функция преобразует html в string"""
    headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64)\
                        AppleWebKit/537.36 (KHTML, like Gecko)\
                        Chrome/106.0.0.0 Safari/537.36'
        }
    try:
        result = requests.get(url, headers=headers)
        # проверка статуса соединения, выдает exception если будут ошибки
        result.raise_for_status()
        return result.text
    except (requests.RequestException, ValueError):

        print("Сетевая ошибка")
        return False


def save_news(title, url, published):
    news_exists = News.query.filter(News.url == url)
    if not news_exists:
        news_news = News(title=title, url=url, published=published)
        db.session.add(news_news)
        db.session.commit()
