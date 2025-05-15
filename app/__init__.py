from flask import Flask
from .routes.api import api_bp
import os
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())

from flask import Flask


def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')
    app.config["DEBUG"] = os.environ.get('FLASK_DEBUG')
    app.config["FLASK_ENV"] = os.environ.get('FLASK_ENV')
    app.register_blueprint(api_bp, url_prefix='/api')
    return app

