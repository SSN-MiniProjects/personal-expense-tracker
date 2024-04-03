import os

import psycopg2
from flask import Flask
from flask_login import LoginManager


class SingletonClass(object):
    instance = None

    def __new__(cls):
        if cls.instance is None:
            cls.instance = super(SingletonClass, cls).__new__(cls)
        return cls.instance


class LoginManagerFlask(SingletonClass):
    def __init__(self):
        self.instance = LoginManager()


class AppFlask(SingletonClass):

    def __init__(self):
        self.instance = Flask(__name__,
                              template_folder="../templates",
                              static_folder="../static")
