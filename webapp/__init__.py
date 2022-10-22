from flask import Flask, render_template
from webapp.python_news import get_python_news
from webapp.model import db, News
from webapp.weather import weather_by_city


def create_app():
    """Функция инициализации flask приложения"""
    app = Flask(__name__)
    app.config.from_pyfile('config.py')  # указываем приложению где брать конфигурационные данные
    db.init_app(app)

    with app.app_context():
        # db.create_all()  # создаем базу данных один раз
        get_python_news()  # заполняем данными базу данных

    @app.route("/")
    def index():
        page_title = "Новости Python"
        weather = weather_by_city(app.config['WEATHER_DEFAULT_CITY'])
        news_list = News.query.order_by(News.published.desc()).all()
        return render_template('index.html', page_title=page_title, weather=weather, news_list=news_list)

    return app
