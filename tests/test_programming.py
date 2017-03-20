from unittest.mock import patch

from tests.fixtures import mock_vt_ed, mock_eots_ed
from vpr_alexa import programs


@patch('vpr_alexa.programs._get_feed', return_value=mock_vt_ed)
def test_latest_vt_edition(mock):
    """
    Make sure we can fetch the latest episode from the podcast feed and get
    its metadata
    """
    program = programs.latest_episode('vermont edition')
    assert program.name == 'Vermont Edition'
    assert program.title == 'This is a pretend Vermont Edition'
    assert program.text == 'This episode is pretty good.'
    assert program.url == 'https://cpa.ds.npr.org/vpr/audio/2017/03/vted.mp3'
    img_url = 'https://static.feedpress.it/logo/vpr-vermont-edition.jpg'
    assert program.small_img == img_url
    assert program.large_img == img_url


@patch('vpr_alexa.programs._get_feed', return_value=mock_eots_ed)
def test_latest_eye_on_the_sky(mock):
    """
    Make sure we can fetch the latest episode from the podcast feed and get
    its metadata
    """
    program = programs.latest_episode('eye on the sky')
    assert program.name == 'Eye on the Sky'
    assert program.title == 'This is a pretend Eye on the Sky'
    assert program.text == 'This episode is pretty good.'
    assert program.url == 'https://cpa.ds.npr.org/vpr/audio/2017/03/eots.mp3'
    img_url = 'https://static.feedpress.it/logo/vpr-eye-on-the-sky.jpg'
    assert program.small_img == img_url
    assert program.large_img == img_url
