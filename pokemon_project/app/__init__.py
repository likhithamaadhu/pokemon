# Below are built import
import logging

# Below are installed import
from flask import Flask
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

# Below are custom imports
from app import config


app = Flask(__name__)

app.config.from_object(config.Config)
app.logger.setLevel(logging.INFO)

db = SQLAlchemy(app)
migrate = Migrate(app, db)

from app import views

app.register_blueprint(views.pokemon_api)
