from flask import Flask
from flask_login import LoginManager

from webapp.db import db
from webapp.admin.views import blueprint as admin_blueprint
from webapp.news.views import blueprint as news_blueprint
from webapp.user.models import User
from webapp.user.views import blueprint as user_blueprint


def create_app():
    """Функция инициализации flask приложения"""
    app = Flask(__name__)
    app.config.from_pyfile('config.py')  # указываем приложению где брать конфигурационные данные
    db.init_app(app)

    login_manager = LoginManager()  # создаем экземляр логин менеджера
    login_manager.init_app(app)  # инициализируем его с приложением
    login_manager.login_view = 'user.login'  # указываем какая функция будет отображать процесс авторизации
    app.register_blueprint(admin_blueprint)
    app.register_blueprint(news_blueprint)
    app.register_blueprint(user_blueprint)  # регистрация user_blueprint в приложении

    @login_manager.user_loader  # логин менеждер вытаскивает из сессионной куки user_id, 
    def load_user(user_id):     # затем функция возвращает пользователя с таким id
        return User.query.get(user_id)

    return app
