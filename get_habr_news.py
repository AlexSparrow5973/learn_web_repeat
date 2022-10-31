from webapp import create_app
from webapp.news.parsers.habr import get_habr_snippets, get_habr_content_news

app = create_app()

with app.app_context():
    # get_habr_snippets()
    get_habr_content_news()
