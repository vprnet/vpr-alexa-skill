"""
Tests for VPR's Amazon Alexa Skill
"""
from vpr_alexa.webapp import create_app
from tests.fixtures import mock_vted_program
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
    return app.test_client()


def post(flask_client, request):
    response = flask_client.post('/ask', data=request)
    assert response.status_code == 200
    return json.loads(response.data.decode('utf-8'))


def test_welcome(client):
    response = post(client, requests.launch())

    assert response['response']['shouldEndSession'] is False
    assert 'Welcome to Vermont Public Radio' \
           in response['response']['outputSpeech']['text']
    assert 'You can say ' \
           in response['response']['reprompt']['outputSpeech']['text']
    assert 'Play the latest Vermont Edition or List Programs' \
           in response['response']['reprompt']['outputSpeech']['text']


def test_program_list(client):
    response = post(client, requests.list_programs())

    assert response['response']['shouldEndSession'] is False
    assert 'You can listen to the following programs' \
           in response['response']['outputSpeech']['text']
    assert 'Which would you like to listen to? ' \
           'You can say the name of the program or cancel.'\
           in response['response']['outputSpeech']['text']


@patch('vpr_alexa.programs.latest_vt_edition', return_value=mock_vted_program)
def test_play_program(mock, client):
    response = post(client, requests.play_program('vermont edition'))

    assert 'Playing the latest Vermont Edition ' \
           'This is a pretend Vermont Edition' \
           in response['response']['outputSpeech']['text']
    assert 'AudioPlayer.Play' in response['response']['directives'][0]['type']

    card = response['response']['card']
    assert card['title'] == 'Vermont Edition'
    assert 'This is a pretend Vermont Edition' in card['text']
    assert 'This episode is pretty good' in card['text']
    assert 'image' in card
    assert len(card['image']) == 2


def test_request_bad_program(client):
    response = post(client, requests.play_program())

    assert 'Sorry' in response['response']['outputSpeech']['text']

