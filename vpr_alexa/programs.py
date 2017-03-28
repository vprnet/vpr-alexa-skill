# -*- coding: utf-8 -*-
"""
VPR Programming

Includes functions for creating VPR Programs and getting latest metadata.
"""
from collections import namedtuple
import feedparser

Program = namedtuple('Program',
                     ['name', 'title', 'text', 'url',
                      'small_img', 'large_img', 'is_podcast'])

podcasts = {'vermont-edition', 'eye-on-the-sky', 'vpr-news'}

# List of Streaming Programs with metadata.
radio = Program(name='Vermont Public Radio', title='Vermont Public Radio Live Stream',
                url='https://vpr.streamguys1.com/vpr96.mp3',
                text="Vermont's NPR News Source",
                small_img='https://mediad.publicbroadcasting.net/p/vpr/files/live-stream-logo.png',
                large_img='https://mediad.publicbroadcasting.net/p/vpr/files/live-stream-logo.png',
                is_podcast=False)

jazz = Program(name='VPR Jazz', title='VPR Jazz Live Stream',
               url='https://vprjazz.streamguys1.com/vpr64-mobile.mp3',
               text="Jazz24 features the greatest jazz artists of all time, like Miles Davis, Billie Holiday and Dave Brubeck; as well as today’s top talents, like Wynton Marsalis, Diana Krall and Pat Metheny. You'll also find some surprises from time to time, seasoning the jazz gumbo with blues, funk and Latin jazz.",
               small_img='https://mediad.publicbroadcasting.net/p/vpr/files/jazz-logo.png',
               large_img='https://mediad.publicbroadcasting.net/p/vpr/files/jazz-logo.png',
               is_podcast=False)

classical = Program(name='VPR Classical', title='VPR Classical Live Stream',
                    url='https://vprclassical.streamguys1.com/vprclassical64-mobile.mp3',
                    text="VPR Classical is Vermont's statewide classical music station. We bring you the broad world of classical music with a strong local connection: local hosts throughout the week, live performances, news about events in your community, and more.",
                    small_img='https://mediad.publicbroadcasting.net/p/vpr/files/classical-logo.png',
                    large_img='https://mediad.publicbroadcasting.net/p/vpr/files/classical-logo.png',
                    is_podcast=False)


def _filter_links(links, link_type):
    """
    Filters a list of RSS links by a given type value (e.g. audio/mpeg)
    :param links: list of link dicts from RSS feed
    :param type: string value of link type (e.g. "audio/mpeg")
    :return: list of matching links
    """
    for link in links:
        if 'type' in link:
            if link['type'] == link_type:
                yield link


def _get_feed(url):
    """
    Wrapper around Feedparser's parse call. Caching could go here in the future.

    :param url: url to RSS feed to fetch and parse
    :return: new dict of RSS feed results
    """
    return dict(feedparser.parse(url))


def latest_podcast_episode(podcast_name):
    """
    Fetch the latest podcast episode from https://podcasts.vpr.net
    :param podcast_name: url-style name of the podcast, e.g. "vermont-edition"
    :return: new Program named tuple with episode metadata
    """
    if podcast_name in podcasts:
        feed = _get_feed('https://podcasts.vpr.net/' + podcast_name)
        if feed:
            latest = feed['entries'][0]
            title = latest['title']
            text = latest['summary']
            links = list(_filter_links(latest['links'], 'audio/mpeg'))
            img_url = feed['feed']['image']['href']
            return Program(name=feed['feed']['title'],
                           url=links[0]['href'],
                           title=title,
                           text=text,
                           small_img=img_url,
                           large_img=img_url,
                           is_podcast=True)


def get_program(program_name):
    """
    Get the latest episode for a given VPR program by name.
    :param program_name: a valid program name (see program_list)
    :return: new Program named tuple
    """
    if program_name:
        program_name = program_name.lower()
    else:
        program_name = ''

    if 'edition' in program_name or 'addition' in program_name:
        return latest_podcast_episode('vermont-edition')
    elif 'sky' in program_name or 'weather' in program_name:
        eots = latest_podcast_episode('eye-on-the-sky')
        if str(eots.url).startswith('http://'):
            # named tuples are immutable, but have a built in _replace method
            # that lets you create a new instance with modified data.
            eots = eots._replace(url=str(eots.url).replace('http:', 'https:'))
        return eots
    elif 'jazz' in program_name:
        return jazz
    elif 'classical' in program_name:
        return classical
    elif 'news' in program_name:
        return latest_podcast_episode('vpr-news')
    else:
        return radio
