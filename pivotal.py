import settings
import objects
import urllib2
import urllib
from lxml import etree

STORIES_URL = 'https://www.pivotaltracker.com/services/v3/projects/{0}/stories?{1}'

def get_url(url, guid):
    """Get the provided url using the provided guid"""
    req = urllib2.Request(url)
    req.add_header('X-TrackerToken', guid)
    data = etree.parse(urllib2.urlopen(req))
    return data

def get_stories_by_filter(project_id, some_filter):
    formatted_url = STORIES_URL.format(project_id, urllib.urlencode(some_filter))
    data = get_url( formatted_url, settings.guid )
    return objects.Story.parse(data)
    
def get_bugs(project_id):
    return get_stories_by_filter(project_id, {"filter": "type:bug"})
    
