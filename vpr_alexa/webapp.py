"""
Vermont Public Radio Alexa Skill
"""
import os
from flask import Flask, Blueprint, render_template, make_response
from flask_ask import Ask, question, statement, audio
from vpr_alexa import programs, logger

ASK_ROUTE = '/ask'
alexa = Blueprint('alexa', __name__)
ask = Ask(route=ASK_ROUTE)


@ask.launch
def welcome():
    """
    General launch intent briefing the user on what the skill provides.
    :return: question for specific intent to either get program list or play a
    particular program
    """
    logger.info("welcome launch")
    return question(render_template('welcome'))\
        .reprompt(render_template('welcome_reprompt'))


@ask.intent('ListPrograms')
def list_programs():
    """
    Program listing menu. Should tell the users the available programming and
    prompt for a selection.
    :return: question of which program to play
    """
    logger.info("list programs launch")
    return question(render_template('list_programs'))


@ask.intent('PlayProgram', mapping={'program_name': 'ProgramName'})
def play_program(program_name=''):
    """
    Our key intent for playing audio.
    :param program_name: ProgramName slot value from LIST_OF_PROGRAMS or close
    enough values.
    :return: audio directive on successful program selection, statement on error
    """
    logger.info("play program launch (program_name: %s)" % program_name)

    try:
        program = programs.get_program(program_name.lower())

        if program.is_podcast:
            speech = render_template('play_podcast', name=program.name,
                                     title=program.title)
        else:
            speech = render_template('play_livestream', name=program.name)

        return audio(speech) \
            .play(program.url) \
            .standard_card(title=program.title, text=program.text,
                           small_image_url=program.small_img,
                           large_image_url=program.large_img)

    except Exception as e:
        logger.error('Failed to launch program for program_name: %s'
                     % program_name)
        logger.info('Exception: %s' % e)

    return statement('Sorry, I did not understand your request!')


@ask.intent('SelectProgram', mapping={'program_name': 'ProgramName'})
def select_program(program_name):
    return play_program(program_name)


@ask.intent('AMAZON.HelpIntent')
def help():
    return question(render_template('help'))


@ask.on_playback_started()
def started(offset, token):
    """
    The skill gets notified when the stream's about to start. This allows for
    any state handling, but also for now is just helpful for debugging.
    """
    logger.info('Playback started at %d ms for token %s' % (offset, token))


@ask.on_playback_stopped()
def stopped(offset, token):
    """
    The skill gets notified when the stream is stopped. This allows for
    any state handling, but also for now is just helpful for debugging.
    """
    logger.info('Playback stopped at %d ms for token %s' % (offset, token))


@ask.intent('AMAZON.PauseIntent')
def pause():
    """
    Suspends playback of Audio. Should be resume-able via AMAZON.ResumeIntent
    """
    logger.info('pausing a stream')
    return audio('Pausing').stop()


@ask.intent('AMAZON.ResumeIntent')
def resume():
    """
    Resume a paused audio stream.
    """
    logger.info('resuming a stream')
    return audio('Resuming').resume()


@ask.intent('AMAZON.StopIntent')
def stop_session():
    """
    This doesn't seem to be a thing or at least not what you'd expect. Usually
    AMAZON.PauseIntent is the actual stopping of audio.
    """
    logger.info('stop requested')
    # return statement('Thanks for listening!')


@ask.intent('AMAZON.CancelIntent')
def cancel_session():
    logger.info('cancel requested')
    return statement('')


@ask.session_ended
def session_ended():
    logger.info('ending session')
    return make_response()


def create_app():
    """
    Initialize a Flask web application instance and wire up our Alexa blueprint
    :return: new instance of Flask
    """
    app = Flask(__name__)
    if 'FLASK_SECRET_KEY' not in os.environ:
        logger.info('!!! No FLASK_SECRET_KEY set in environment')
        logger.info('Please set the FLASK_SECRET_KEY in the systems environment'
                    ' settings and restart the application.')
        return None

    app.secret_key = os.environ['FLASK_SECRET_KEY']
    if 'FLASK_DEBUG' in os.environ:
        app.debug = True
    if 'DISABLE_ASK_VERIFY_REQUESTS' in os.environ:
        if os.environ['DISABLE_ASK_VERIFY_REQUESTS'].lower() == 'true':
            logger.info('!!! Disabling ASK Request verification')
            app.config['ASK_VERIFY_REQUESTS'] = False

    app.register_blueprint(alexa)
    ask.init_app(app)

    return app
