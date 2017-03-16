"""
Flask-Ask based web app
"""
import os
from flask import Flask, Blueprint, render_template
from flask_ask import Ask, question, statement, audio, current_stream
from vpr_alexa import programs, logger

ASK_ROUTE = '/ask'
alexa = Blueprint('alexa', __name__)
ask = Ask(route=ASK_ROUTE)


@ask.launch
def welcome():
    logger.info("welcome launch")
    return question(render_template('welcome'))\
        .reprompt(render_template('welcome_reprompt'))


@ask.intent('ListPrograms')
def list_programs():
    logger.info("list programs launch")
    return question(render_template('list_programs'))


@ask.intent('PlayProgram')
def play_program(program_name=''):
    logger.info("play program launch (program_name: %s)" % program_name)

    if program_name.lower() == 'vermont edition':
        program = programs.latest_vt_edition()
    else:
        program = None

    if program:
        speech = render_template('play_program', program_name=program.title)
        return audio(speech).play(program.url)
    else:
        return statement('Sorry, I did not understand your request!')


@ask.intent('AMAZON.PauseIntent')
def pause():
    logger.info('Pausing current stream: %s' % current_stream.url)
    return audio().stop()


@ask.intent('AMAZON.ResumeIntent')
def resume():
    logger.info('Resuming current stream: %s' % current_stream.url)
    return audio().resume()


@ask.intent('AMAZON.CancelIntent')
def cancel_session():
    return statement('Thanks for listening!')

@ask.session_ended
def session_ended():
    return "", 200


def create_app():
    """
    Initialize a Flask web application instance and wire up our Alexa blueprint
    :return: new instance of Flask
    """
    app = Flask(__name__)
    if 'FLASK_SECRET_KEY' not in os.environ:
        logger.warn('!!! No FLASK_SECRET_KEY set in environment')
        logger.info('Please set the FLASK_SECRET_KEY in the systems environment'
                    ' settings and restart the application.')
        return None

    app.secret_key = os.environ['FLASK_SECRET_KEY']
    if 'FLASK_DEBUG' in os.environ:
        app.debug = True
    if 'DISABLE_ASK_VERIFY_REQUESTS' in os.environ:
        if os.environ['DISABLE_ASK_VERIFY_REQUESTS'].lower() == 'true':
            logger.warn('!!! Disabling ASK Request verification')
            app.config['ASK_VERIFY_REQUESTS'] = False

    app.register_blueprint(alexa)
    ask.init_app(app)

    return app
