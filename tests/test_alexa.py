"""
Tests against VPR's Amazon Alexa Skill webapp logic.
"""
from vpr_alexa.webapp import create_app, stream_cache
from vpr_alexa.programs import jazz
from tests.fixtures import *
import tests.requests as requests

from mock import patch
from pytest import fixture
import json
import os

if 'FLASK_SECRET_KEY' not in os.environ:
    os.environ.setdefault('FLASK_SECRET_KEY', 'asdf')

app = create_app()
app.config['ASK_VERIFY_REQUESTS'] = False
app.config['TESTING'] = True


@fixture(name='client')
def setup_client():
    """
    Configure our test fixture. Your test functions should have a 'client'
    parameter to allow using the pytest fixture.
    :return: Flask test client
    """
    return app.test_client()


def post(flask_client, request):
    """
    Helper function for sending the recorded JSON to our Flask app.
    :param flask_client: Flask test_client
    :param request: file descriptor to JSON input
    :return: Python object deserialized from resulting JSON response
    """
    response = flask_client.post('/ask', data=request)
    assert response.status_code == 200
    return json.loads(response.data.decode('utf-8'))


def test_welcome(client):
    """
    Test our general welcome/launch intent. Do we get the prompt and question?
    """
    response = post(client, requests.launch())

    assert response['response']['shouldEndSession'] is False
    assert 'Welcome to Vermont Public Radio' \
           in response['response']['outputSpeech']['text']
    assert 'You can say ' \
           in response['response']['reprompt']['outputSpeech']['text']
    assert 'Play the latest Vermont Edition or List Programs' \
           in response['response']['reprompt']['outputSpeech']['text']


def test_program_list(client):
    """
    Can we get the program listing?
    """
    response = post(client, requests.list_programs())

    assert response['response']['shouldEndSession'] is False
    assert 'You can listen to the following' \
           in response['response']['outputSpeech']['text']
    assert 'Which would you like to listen to? ' \
           'You can say the name of the program or cancel.'\
           in response['response']['outputSpeech']['text']


@patch('vpr_alexa.programs.get_program', return_value=mock_vted_program)
def test_play_program(mock, client):
    """
    Can we play a VT Edition and get the resulting Card?
    :param mock: mock VT Edition Program
    :param client: Flask test client
    """

    response = post(client, requests.play_program("vermont edition"))
    assert 'Playing the latest Vermont Edition titled ' \
           'This is a pretend Vermont Edition' \
           in response['response']['outputSpeech']['text']
    assert 'AudioPlayer.Play' in response['response']['directives'][0]['type']

    card = response['response']['card']
    assert card['title'] == 'This is a pretend Vermont Edition'
    assert 'This episode is pretty good' in card['text']
    assert 'image' in card
    assert len(card['image']) == 2


@patch('vpr_alexa.programs.get_program', return_value=mock_eots_program)
def test_eots(mock, client):
    """
    Can we play Eye on the Sky and get the resulting card?
    :param mock: mock Eye on the Sky Program
    :param client: Flask test client
    """
    response = post(client, requests.play_program("eye on the sky"))
    assert 'Playing the latest Eye on the Sky titled ' \
           'This is a pretend Eye on the Sky' \
           in response['response']['outputSpeech']['text']
    assert 'AudioPlayer.Play' in response['response']['directives'][0]['type']

    card = response['response']['card']
    assert card['title'] == 'This is a pretend Eye on the Sky'
    assert 'This episode is pretty good' in card['text']
    assert 'image' in card
    assert len(card['image']) == 2


@patch('vpr_alexa.programs.get_program', return_value=mock_jazz_program)
def test_stream(mock, client):
    """
    When we play a live stream do we get appropriate verbiage?
    :param mock:
    :param client:
    :return:
    """
    response = post(client, requests.play_program('jazz'))
    assert 'Playing the live stream for VPR Jazz' \
           in response['response']['outputSpeech']['text']
    assert 'AudioPlayer.Play' in response['response']['directives'][0]['type']

    card = response['response']['card']
    assert card['title'] == 'VPR Jazz Live Stream'
    assert "Jazz24 features the greatest jazz artists" in card['text']
    assert 'image' in card
    assert len(card['image']) == 2


def test_request_bad_program(client):
    response = post(client, requests.play_program())

    assert 'Vermont Public Radio' in response['response']['outputSpeech']['text']


def test_cancel_quits_session(client):
    """
    User should be able to cancel the interaction according to Amazon
    :param client:
    :return:
    """
    response = post(client, requests.cancel())
    assert response['response']['shouldEndSession']
    assert response['response']['outputSpeech']['text'] == ''


def test_help_intent(client):
    """
    Users need to receive a special help prompt when asking for help.
    :param client:
    :return:
    """
    response = post(client, requests.help())
    assert response['response']['shouldEndSession'] is False
    assert 'I can help you listen to your favorite Vermont Public Radio' in \
           response['response']['outputSpeech']['text']


def test_saying_nothing_silently_ends_session(client):
    """
    A non-response (dead air) should just end the session. Amazon dictates that
    the response to a SessionEnd request should be empty (no actual json)
    :param client:
    :return:
    """
    response = client.post('/ask', data=requests.say_nothing())
    assert response.status_code == 200
    assert response.data == b"{}"


def test_saves_tokens(client):
    """
    Test that we can start and stop streams and preserve tokens.
    """
    response =  post(client, requests.play_program('jazz'))
    token = response['response']['directives'][0]['audioItem']['stream']['token']
    
    post(client, requests.playback_started(token))

    assert token in stream_cache
    assert stream_cache[token] == jazz.url
    
