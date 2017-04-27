"""
Test fixtures for simulating JSON input from Alexa.

These functions consolidate the logic for reading the fixture json
files from disk and properly returning a File-like object for
passing directly to things like Flask's `test_client`, which requires
a File-like object for reading the POST data to send.

"""
import os
import io
import six

requests_dir = os.path.realpath(os.path.join(os.path.realpath(__file__),
                                             '../fixtures/'))


def _read_request_json(filename):
    with open(requests_dir + '/' + filename, 'r') as f:
        body = f.read()
        return io.StringIO(six.u(body))


def launch():
    return _read_request_json('launch.json')


def list_programs():
    return _read_request_json('list_programs.json')


def play_program(program='totally not a program'):
    json = _read_request_json('play_program.json').read()
    return io.StringIO(json.replace('{{VALUE}}', program))


def cancel():
    return _read_request_json('cancel.json')


def help():
    return _read_request_json('help.json')


def say_nothing():
    return _read_request_json('say_nothing.json')
