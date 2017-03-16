"""
VPR Programming
"""
from collections import namedtuple

Program = namedtuple('Program', ['url', 'title'])


def latest_vt_edition():
    return Program('https://cpa.ds.npr.org/vpr/audio/2017/03/vermont-edition-20170315.mp3', 'Vermont Edition')