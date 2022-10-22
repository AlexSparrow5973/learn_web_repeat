from getpass import getpass
import sys

from webapp import create_app
from webapp.model import db, User

app = create_app()  # создаем приложение

with app.app_context():  # в контексте приложения запрашиваем имя пльзователя
    username = input("Введите имя: ")

    if User.query.filter(User.username==username).count():  # проверяем есть такой пользователь в базе
        print("Такой пользователь уже существует")
        sys.exit(0)

    password1 = getpass("Введите пароль: ")
    password2 = getpass("Повторите пароль: ")

    if not password1 == password2:
        print("Пороли не совпадают")
        sys.exit(0)

    new_user = User(username=username, role="admin")  # создаем экземпляр класса User с ролью "админ"
    new_user.set_password(password1)  # хеш пароля

    db.session.add(new_user)  # добавляем админа в базу
    db.session.commit()
    print("Создан пользователь с id={}".format(new_user.id))
