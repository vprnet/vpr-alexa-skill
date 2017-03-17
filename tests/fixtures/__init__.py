"""
Various test fixtures
"""
from vpr_alexa.programs import Program

mock_vt_ed = {'entries': [{
    'title': 'This is a pretend Vermont Edition',
    'links': [
        {'type': 'junk'},
        {'type': 'audio/mpeg',
         'href': 'https://cpa.ds.npr.org/vpr/audio/2017/03/vted.mp3'}
    ]
}]}

mock_vted_program = \
    Program(name='Vermont Edition',
            title='This is a pretend Vermont Edition',
            url='https://cpa.ds.npr.org/vpr/audio/2017/03/vted.mp3',
            small_img='https://static.feedpress.it/logo/vpr-vermont-edition.jpg',
            large_img='https://static.feedpress.it/logo/vpr-vermont-edition.jpg')
