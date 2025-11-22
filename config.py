import os

class Config:
    SECRET_KEY = "kajfj98akjfksdjf923jfdskuf9238ryjksdnfksdhdf"
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///mcq_app.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
