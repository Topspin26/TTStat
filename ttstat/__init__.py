from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from .models import TTModel

ttstat = Flask(__name__)
#ttstat.config.from_object('config')
#db = SQLAlchemy(mytable)
ttModel = TTModel('D:/Programming/SportPrognoseSystem/TTStat')

from ttstat import views