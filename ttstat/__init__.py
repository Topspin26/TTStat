from flask import Flask
import psycopg2
# from flask_sqlalchemy import SQLAlchemy
from flask_apscheduler import APScheduler
from .models import TTModel
from.presenter import Presenter
from PredictionMachine import PredictionMachine
from config import *

ttstat = Flask(__name__)
ttstat.config.from_object('config')
# db = SQLAlchemy(mytable)
ttModel = TTModel('C:/Programming/SportPrognoseSystem/TTStat')

predictionMachine = PredictionMachine()
ttModel.setPredictionMachine(predictionMachine)

ttPresenter = Presenter(ttModel)

db = psycopg2.connect("dbname='{}' user='{}' password='{}'".format(ttstat.config.get('DB_NAME'),
                                                                   ttstat.config.get('DB_USER'),
                                                                   ttstat.config.get('DB_PASSWORD')))

from ttstat import views

scheduler = APScheduler()
scheduler.init_app(ttstat)
scheduler.start()
