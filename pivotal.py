import urllib2
from lxml import etree

def get_url(url, guid):
    """Get the provided url using the provided guid"""
    req = urllib2.Request(url)
    req.add_header('X-TrackerToken', guid)
    data = etree.parse(urllib2.urlopen(req))
    return data
