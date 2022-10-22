from flask import Flask, render_template, redirect, flash, url_for
from flask_login import LoginManager, current_user, login_required ,login_user, logout_user
from webapp.forms import LoginForm
from webapp.model import db, News, User
from webapp.weather import weather_by_city


def create_app():
    """Функция инициализации flask приложения"""
    app = Flask(__name__)
    app.config.from_pyfile('config.py')  # указываем приложению где брать конфигурационные данные
    db.init_app(app)

    login_manager = LoginManager()  # создаем экземляр логин менеджера
    login_manager.init_app(app)  # инициализируем его с приложением
    login_manager.login_view = 'login'  # указываем какая функция будет отображать процесс авторизации

    @login_manager.user_loader  # логин менеждер вытаскивает из сессионной куки user_id, 
    def load_user(user_id):     # затем функция возвращает пользователя с таким id
        return User.query.get(user_id)


    @app.route('/')
    def index():
        title = "Новости Python"
        weather = weather_by_city(app.config['WEATHER_DEFAULT_CITY'])
        news_list = News.query.order_by(News.published.desc()).all()
        return render_template('index.html', page_title=title, weather=weather, news_list=news_list)

    @app.route('/login')
    def login():
        if current_user.is_authenticated:
            flash('Вы уже авторизовались')
            return redirect(url_for('index'))
        title = "Авторизация"
        login_form = LoginForm()
        return render_template('login.html', page_title=title, form=login_form)

    @app.route('/process-login', methods=['POST'])
    def process_login():
        form = LoginForm()

        if form.validate_on_submit():
            user = User.query.filter_by(username=form.username.data).first()
            if user and user.check_password(form.password.data):
                login_user(user)
                flash('Вы успешно вошли на сайт')
                return redirect(url_for('index'))
            flash('Неправильное имя пользователя или пароль')
            return redirect(url_for('login'))

    @app.route('/logout')
    def logout():
        logout_user()
        flash('Вы успешно разлогинились')
        return redirect(url_for('index'))

    @app.route('/admin')
    @login_required
    def admin():
        if current_user.is_admin:
            return "Привет админ"
        return "Ты не админ"

    return app
