"""
VPR Programming

Includes functions for creating VPR Programs and getting latest metadata.
"""
from collections import namedtuple
import feedparser

Program = namedtuple('Program',
                     ['name', 'title', 'text', 'url', 'small_img', 'large_img'])

podcasts = {'vermont-edition', 'eye-on-the-sky', 'vpr-news'}


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
                           large_img=img_url)


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
    elif 'sky' in program_name:
        return latest_podcast_episode('eye-on-the-sky')
    elif 'jazz' in program_name:
        return Program(name='VPR Jazz', title='VPR Jazz Live Stream',
                       url='https://vprjazz.streamguys1.com/vpr64-mobile.mp3',
                       text='VPR Jazz Live Stream',
                       small_img='https://placehold.it/300?text=Jazz',
                       large_img='https://placehold.it/600?text=Jazz')
    elif 'classical' in program_name:
        return Program(name='VPR Classical', title='VPR Classical Live Stream',
                       url='https://vprclassical.streamguys1.com/vprclassical64-mobile.mp3',
                       text='VPR Classical Live Stream',
                       small_img='https://placehold.it/300?text=Classical',
                       large_img='https://placehold.it/600?text=Classical')
    elif 'news' in program_name:
        return latest_podcast_episode('vpr-news')
    else:
        return Program(name='Vermont Public Radio', title='VPR Live Stream',
                       url='https://vpr.streamguys1.com/vpr96.mp3',
                       text="Vermont's NPR News Source",
                       small_img='https://pbs.twimg.com/profile_images/519508312606248960/bYpREhMx.png',
                       large_img='https://pbs.twimg.com/profile_images/519508312606248960/bYpREhMx.png')

