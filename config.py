import os
from dotenv import load_dotenv

basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir, '.env'))

class Config(object):
    # secret key used by Flask-WTF to prevent CSRF(Cross-Site Request Forgery)
    SECRET_KEY = os.environ.get('SECRET_KEY')
    # location of app's database.
    # if no database, cofigure new database named app.db in main directory
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///' + os.path.join(basedir, 'app.db')
    # disable signaling to the database every time a change is about to be made
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    MAIL_SERVER = os.environ.get('MAIL_SERVER')
    MAIL_PORT = int(os.environ.get('MAIL_PORT') or 25)
    MAIL_USE_TLS = os.environ.get('MAIL_USE_TLS') is not None
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    ADMINS = ['simpleemailtester@gmail.com', 'dictatorcracker@gmail.com']
    POSTS_PER_PAGE = 3
