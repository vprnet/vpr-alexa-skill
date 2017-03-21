"""
Tests against VPR's Amazon Alexa Skill webapp logic.
"""
from vpr_alexa.webapp import create_app
from tests.fixtures import *
import tests.requests as requests

from unittest.mock import patch
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
    assert 'You can listen to the following programs' \
           in response['response']['outputSpeech']['text']
    assert 'Which would you like to listen to? ' \
           'You can say the name of the program or cancel.'\
           in response['response']['outputSpeech']['text']


@patch('vpr_alexa.programs.latest_episode', return_value=mock_vted_program)
def test_play_program(mock, client):
    """
    Can we play a VT Edition and get the resulting Card?
    :param mock:
    :param client:
    :return:
    """

    response = post(client, requests.play_program("vermont edition"))
    assert 'Playing the latest Vermont Edition titled ' \
           'This is a pretend Vermont Edition' \
           in response['response']['outputSpeech']['text']
    assert 'AudioPlayer.Play' in response['response']['directives'][0]['type']

    card = response['response']['card']
    assert card['title'] == 'Vermont Edition: This is a pretend Vermont Edition'
    assert 'This episode is pretty good' in card['text']
    assert 'image' in card
    assert len(card['image']) == 2


@patch('vpr_alexa.programs.latest_episode', return_value=mock_eots_program)
def test_eots(mock, client):
    """
    Can we play Eye on the Sky and get the resulting card?
    :param mock:
    :param client:
    :return:
    """
    response = post(client, requests.play_program("eye on the sky"))
    assert 'Playing the latest Eye on the Sky titled ' \
           'This is a pretend Eye on the Sky' \
           in response['response']['outputSpeech']['text']
    assert 'AudioPlayer.Play' in response['response']['directives'][0]['type']

    card = response['response']['card']
    assert card['title'] == 'Eye on the Sky: This is a pretend Eye on the Sky'
    assert 'This episode is pretty good' in card['text']
    assert 'image' in card
    assert len(card['image']) == 2




def test_request_bad_program(client):
    response = post(client, requests.play_program())

    assert 'Sorry' in response['response']['outputSpeech']['text']
