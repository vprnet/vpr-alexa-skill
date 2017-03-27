"""
Various test fixtures
"""
from vpr_alexa.programs import Program

# These dicts are our expected formats for parsed RSS feeds.
mock_vt_ed = {
    'feed': {
        'title': 'Vermont Edition',
        'image': {
            'href': 'https://static.feedpress.it/logo/vpr-vermont-edition.jpg'
        }
    },
    'entries': [{
        'title': 'This is a pretend Vermont Edition',
        'summary': 'This episode is pretty good.',
        'links': [
            {'type': 'junk'},
            {'type': 'audio/mpeg',
             'href': 'https://cpa.ds.npr.org/vpr/audio/2017/03/vted.mp3'}
            ]
    }]
}


mock_eots_ed = {
    'feed': {
        'title': 'Eye on the Sky',
        'image': {
            'href': 'https://static.feedpress.it/logo/vpr-eye-on-the-sky.jpg'
        }
    },
    'entries': [{
        'title': 'This is a pretend Eye on the Sky',
        'summary': 'This episode is pretty good.',
        'links': [
            {'type': 'junk'},
            {'type': 'audio/mpeg',
             'href': 'https://cpa.ds.npr.org/vpr/audio/2017/03/eots.mp3'}
        ]
}]}


# These Program named tuples are used for mock inputs.

mock_vted_program = \
    Program(name='Vermont Edition',
            title='This is a pretend Vermont Edition',
            text='This episode is pretty good.',
            url='https://cpa.ds.npr.org/vpr/audio/2017/03/vted.mp3',
            small_img='https://static.feedpress.it/logo/vpr-vermont-edition.jpg',
            large_img='https://static.feedpress.it/logo/vpr-vermont-edition.jpg',
            is_podcast=True)


mock_eots_program = \
    Program(name='Eye on the Sky',
            title='This is a pretend Eye on the Sky',
            text='This episode is pretty good.',
            # eye on the sky currently has a non-https url listed in the feed
            url='http://cpa.ds.npr.org/vpr/audio/2017/03/eots.mp3',
            small_img='https://static.feedpress.it/logo/eots.jpg',
            large_img='https://static.feedpress.it/logo/eots.jpg',
            is_podcast=True)


mock_jazz_program = \
    Program(name='VPR Jazz',
            title='VPR Jazz Live Stream',
            text='Jazz24 features the greatest jazz artists',
            url='https://jazzstream.mp3',
            small_img='https://jazzimage.png',
            large_img='https://jazzimage.png',
            is_podcast=False)