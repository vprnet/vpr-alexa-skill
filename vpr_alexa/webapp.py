"""
Flask-Ask based web app
"""
import os
from flask import Flask

def create_app():
    """
    Initialize a Flask web application instance.
    :return: new instance of Flask
    """
    app = Flask(__name__)
    app.secret_key = os.environ['FLASK_SECRET_KEY']
    return app
