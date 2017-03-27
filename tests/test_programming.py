"""
Tests against the VPR Program logic including fetching Podcasts information.
"""
import os
from unittest.mock import patch

from tests.fixtures import mock_vt_ed, mock_eots_ed
from vpr_alexa import programs


@patch('vpr_alexa.programs._get_feed', return_value=mock_vt_ed)
def test_latest_vt_edition(mock):
    """
    Make sure we can fetch the latest episode from the podcast feed and get
    its metadata
    """
    def check(utterance):
        program = programs.get_program(utterance)
        assert program.name == 'Vermont Edition'
        assert program.title == 'This is a pretend Vermont Edition'
        assert program.text == 'This episode is pretty good.'
        assert program.url == 'https://cpa.ds.npr.org/vpr/audio/2017/03/vted.mp3'
        img_url = 'https://static.feedpress.it/logo/vpr-vermont-edition.jpg'
        assert program.small_img == img_url
        assert program.large_img == img_url
        assert program.is_podcast

    for utterance in ['vermont edition', 'vt edition', 'v t edition',
                      'vermont addition']:
        check(utterance)



@patch('vpr_alexa.programs._get_feed', return_value=mock_eots_ed)
def test_latest_eye_on_the_sky(mock):
    """
    Make sure we can fetch the latest episode from the podcast feed and get
    its metadata
    """
    def check(utterance):
        program = programs.get_program(utterance)
        assert program.name == 'Eye on the Sky'
        assert program.title == 'This is a pretend Eye on the Sky'
        assert program.text == 'This episode is pretty good.'
        assert program.url == 'https://cpa.ds.npr.org/vpr/audio/2017/03/eots.mp3'
        img_url = 'https://static.feedpress.it/logo/vpr-eye-on-the-sky.jpg'
        assert program.small_img == img_url
        assert program.large_img == img_url
        assert program.is_podcast

    for utterance in ['eye on the sky', 'i on the sky',
                      'ion on the sky', 'i am the sky']:
        check(utterance)


def test_alexa_slots_resolve_to_programs():
    """
    Load the LIST_OF_PROGRAMS slot definition file and make sure they all can
    return a Program.

    This does a live hit to the internet, too, and will sanity check VPR's
    current podcast/rss feeds. (e.g. check https)
    """
    path = os.path.join(
        os.path.abspath(os.path.join(programs.__file__, '..')),
        'speech_assets/customSlotTypes/LIST_OF_PROGRAMS')

    with open(path, 'r') as f:
        for line in f.readlines():
            slot = line.strip()

            if slot:
                program = programs.get_program(slot)
                assert program is not None
                for token in slot.split(' '):
                    assert token.lower() in program.name.lower()
                assert program.url.startswith('https')
                assert program.large_img.startswith('https')
                assert program.small_img.startswith('https')
