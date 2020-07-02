from flask import Flask
from flask_mongoengine import MongoEngine
from config import Config
from flask_restful import Api

app = Flask(__name__)
app.config.from_object(Config)

api = Api(app)

db = MongoEngine()
db.init_app(app)

from modules import routes