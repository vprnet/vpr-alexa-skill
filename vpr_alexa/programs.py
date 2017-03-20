"""
VPR Programming

Includes functions for creating VPR Programs and getting latest metadata.
"""
from collections import namedtuple
import feedparser

Program = namedtuple('Program',
                     ['name', 'title', 'text', 'url', 'small_img', 'large_img'])

white_list = set(['vermont-edition', 'eye-on-the-sky'])


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
    if podcast_name in white_list:
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


def latest_episode(program_name):
    """
    Get the latest episode for a given VPR program by name.
    :param program_name: a valid program name (see program_list)
    :return: new Program named tuple
    """
    if program_name == 'vermont edition':
        return latest_podcast_episode('vermont-edition')
    elif program_name == 'eye on the sky':
        return latest_podcast_episode('eye-on-the-sky')

