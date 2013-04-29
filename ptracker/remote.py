import requests
from ptracker.parser import parse

PROJECTS_URL    = 'https://www.pivotaltracker.com/services/v3/projects'
STORIES_URL     = 'https://www.pivotaltracker.com/services/v3/projects/{0}/stories'
STORY_URL       = 'https://www.pivotaltracker.com/services/v3/projects/{0}/stories/{1}'

ACTIVITIES_URL  = 'https://www.pivotaltracker.com/services/v4/stories/{0}/activities?limit=100&page=2'

def _get_data(guid, url_pattern, parameters):
    url = url_pattern.format(*parameters)
    data = requests.get(url, headers={'X-TrackerToken': guid})
    if not data.status_code == 200:
        print(url, data.status_code, data.content)
        raise Exception(data.content)
    return data.content
    
def get_projects(guid):
    xml = _get_data(guid, PROJECTS_URL, ())
    return parse(xml)

def get_stories(guid, project_id):
    xml = _get_data(guid, STORIES_URL, (project_id,))
    return parse(xml)

def get_story(guid, project_id, story_id):
    if not story_id:
        raise Exception("You must specify a story id")

    return parse(_get_data(guid, STORY_URL, (project_id, story_id)))

def get_activities(guid, story_id):
    if not story_id:
        raise Exception("You must specify a story id")

    page = 0
    while True:
        data = _get_data(guid, ACTIVITIES_URL, (story_id, page), 'stories/{0}/activities_{1}.xml')
        page += 1
        if has_story_creation(data):
            break
            
    return parse(data)
