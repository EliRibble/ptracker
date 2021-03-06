import os
import logging
from datetime import datetime
import requests
from ptracker.parser import parse, has_story_creation, num_subitems
from ptracker.configuration import PTRACKER_HOME

PROJECTS_URL    = 'https://www.pivotaltracker.com/services/v3/projects'
STORIES_URL     = 'https://www.pivotaltracker.com/services/v3/projects/{0}/stories'
STORY_URL       = 'https://www.pivotaltracker.com/services/v3/projects/{0}/stories/{1}'

ACTIVITIES_URL  = 'https://www.pivotaltracker.com/services/v4/stories/{0}/activities?limit=100&page={1}'

def _is_outdated(path, max_age=60*60*24):
    try:
        modified_stamp = os.path.getmtime(path)
        modified_date = datetime.fromtimestamp(modified_stamp)
        delta = datetime.now() - modified_date
        return delta.seconds > max_age
    except OSError:
        return True

def _get_contents(path):
    with open(path, 'r') as f:
        return f.read()

def _get_data(guid, url_pattern, parameters, cache_pattern):
    url = url_pattern.format(*parameters)
    cache_file = cache_pattern.format(*parameters)
    cache_file = os.path.join(PTRACKER_HOME, 'cache', cache_file)
    if not _is_outdated(cache_file):
        logging.getLogger('cache').info("Using cached file %s for %s", cache_file, url)
        return _get_contents(cache_file)

    data = requests.get(url, headers={'X-TrackerToken': guid})
    if not data.status_code == 200:
        print(url, data.status_code, data.content)
        raise Exception(data.content)

    if not os.path.exists(os.path.dirname(cache_file)):
        os.makedirs(os.path.dirname(cache_file))
    with open(cache_file, 'w') as cache_output:
        cache_output.write(data.content)
    return data.content
    
def get_projects(guid):
    xml = _get_data(guid, PROJECTS_URL, (), 'projects.xml')
    return parse(xml)

def get_stories(guid, project_id):
    xml = _get_data(guid, STORIES_URL, (project_id,), 'projects/{0}/stories.xml')
    return parse(xml)

def get_story(guid, project_id, story_id):
    if not story_id:
        raise Exception("You must specify a story id")

    d = _get_data(guid, STORY_URL, (project_id, story_id), 'projects/{0}/stories/{1}.xml')
    return parse(d)

def get_activities(guid, story_id):
    if not story_id:
        raise Exception("You must specify a story id")

    page = 0
    while True:
        data = _get_data(guid, ACTIVITIES_URL, (story_id, page), 'stories/{0}/activities_{1}.xml')
        page += 1
        if num_subitems(data) < 100 or has_story_creation(data):
            break
        elif page > 10:
            raise Exception("Probably broken parsing - we're at page %d", page)
            
    return parse(data)
