"""
Flask-Ask based web app
"""
import os
from flask import Flask, Blueprint, render_template
from flask_ask import Ask, question, statement, audio
from vpr_alexa import programs

ASK_ROUTE = '/ask'
alexa = Blueprint('alexa', __name__)
ask = Ask(route=ASK_ROUTE)


@ask.launch
def welcome():
    return question(render_template('welcome'))\
        .reprompt(render_template('welcome_reprompt'))


@ask.intent('ListPrograms')
def list_programs():
    return question(render_template('list_programs'))


@ask.intent('PlayProgram')
def play_program(program_name):
    if program_name == 'vermont edition':
        program = programs.latest_vt_edition()
    else:
        program = None

    if program:
        speech = render_template('play_program', program_name=program.title)
        return audio(speech).play(program.url)
    else:
        return statement('Sorry, I did not understand your request!')


def create_app():
    """
    Initialize a Flask web application instance and wire up our Alexa blueprint
    :return: new instance of Flask
    """
    app = Flask(__name__)
    if 'FLASK_SECRET_KEY' not in os.environ:
        print('### No FLASK_SECRET_KEY set in environment! '
              'Please set the FLASK_SECRET_KEY in the systems environment '
              'settings and restart the application.')
        return None

    app.secret_key = os.environ['FLASK_SECRET_KEY']
    if 'FLASK_DEBUG' in os.environ:
        app.debug = True
    if 'ASK_VERIFY_REQUESTS' in os.environ:
        if os.environ['ASK_VERIFY_REQUESTS'].lower() == 'true':
            print('### Disabling ASK Request verification!!!')
            app.config['ASK_VERIFY_REQUESTS']

    app.register_blueprint(alexa)
    ask.init_app(app)

    return app
