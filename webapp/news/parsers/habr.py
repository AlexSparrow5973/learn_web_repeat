from datetime import datetime
from bs4 import BeautifulSoup
from webapp.db import db
from webapp.news.models import News
from webapp.news.parsers.utils import get_html, save_news


def get_habr_snippets():
    html = get_html("https://habr.com/ru/search/?q=python&target_type=posts&order=date")
    if html:
        soup = BeautifulSoup(html, "html.parser")
        all_news = soup.find('div', class_='tm-articles-list').findAll('article', class_='tm-articles-list__item')
        for news in all_news:
            news_item = news.find('a', class_="tm-article-snippet__title-link")
            title = news_item.find('span',).text
            url = "https://habr.com" + news_item['href']
            published = news.find('time')['title']
            try:
                published = datetime.strptime(published, '%Y-%m-%d, %H:%M')
            except ValueError:
                published = datetime.now()
            save_news(title, url, published)


def get_habr_content_news():
    news_without_text = News.query.filter(News.text.is_(None))
    for news in news_without_text:
        html = get_html(news.url)
        if html:
            soup = BeautifulSoup(html, "html.parser")
            news_content = soup.find('div', class_="article-formatted-body").decode_contents()
            if news_content:
                news.text = news_content
                db.session.add(news)
                db.session.commit()
