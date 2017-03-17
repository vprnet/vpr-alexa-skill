"""
VPR Programming
"""
from collections import namedtuple
import feedparser

Program = namedtuple('Program',
                     ['name', 'title', 'url', 'small_img', 'large_img'])


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
    return dict(feedparser.parse('https://podcasts.vpr.net/vermont-edition'))


def latest_vt_edition():
    feed = _get_feed('https://podcasts.vpr.net/vermont-edition')

    if feed:
        latest = feed['entries'][0]
        title = latest['title']
        links = list(_filter_links(latest['links'], 'audio/mpeg'))
        img_url = 'https://static.feedpress.it/logo/vpr-vermont-edition.jpg'
        return Program(name='Vermont Edition',
                       url=links[0]['href'],
                       title=title,
                       small_img=img_url,
                       large_img=img_url)


def latest_episode(program_name):
    """
    Get the latest episode for a given VPR program by name.
    :param program_name: a valid program name (see program_list)
    :return: new Program named tuple
    """
    if program_name == 'vermont edition':
        return latest_vt_edition()
