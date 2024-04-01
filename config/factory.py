import os

import psycopg2
from flask import Flask
from flask_login import LoginManager


class SingletonClass(object):
    instance = None

    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super(SingletonClass, cls).__new__(cls)
        return cls.instance


class LoginManagerFlask(SingletonClass):
    instance = LoginManager()


class AppFlask(SingletonClass):
    instance = Flask(__name__)


class Database(SingletonClass):
    instance = psycopg2.connect(
        dbname=os.getenv("DB_NAME"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASS"),
        host=os.getenv("DB_HOST"),
        port="5432"
    )
