from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager


# create Flask application
app = Flask(__name__)
app.config.from_object(Config)
# create instances for extensions, these onjects need to be created after the application
db = SQLAlchemy(app)
migrate = Migrate(app, db)
login = LoginManager(app)

# import modules to the application
from app import routes, models
