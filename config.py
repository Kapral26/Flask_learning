# -*- coding: utf-8 -*-
import os
basedir = os.path.normpath(os.path.dirname(__file__))


class Config(object):
    SECRET_KEY = os.environ.get("SECRET_KEY") or "you-will-never-guess"
    file_db = os.path.join(basedir, "app.db")
    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL") or f"sqlite:///{file_db}"
    # Параметр сигнализирования при внесений изменений в БД
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    MAIL_SERVER = os.environ.get("MAIL_SERVER") or "smtp.yandex.ru"
    MAIL_PORT = int(os.environ.get("MAIL_PORT") or 587)
    MAIL_USE_TLS = os.environ.get("MAIL_USE_TLS") or True
    # TODO Удалить логин пароль
    MAIL_USERNAME = os.environ.get("MAIL_USERNAME") or "kapral26.prod@yandex.ru"
    MAIL_PASSWORD = os.environ.get("MAIL_PASSWORD")
    ADMINS = ["kapral26.prod@yandex.ru"]
    POSTS_PER_PAGE = 25