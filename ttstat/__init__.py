from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from .models import TTModel

ttstat = Flask(__name__)
#ttstat.config.from_object('config')
#db = SQLAlchemy(mytable)
ttModel = TTModel()

from ttstat import views