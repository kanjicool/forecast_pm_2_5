import mongoengine as me
from flask_mongoengine import MongoEngine
from .users import User
from .forecast_model import load_forecast_model


__all__ = [
    "User",
    "load_forecast_model"
]

db = MongoEngine()

def init_db(app):
    db.init_app(app)