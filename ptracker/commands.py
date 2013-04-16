import requests
from lxml import etree
import StringIO
from ptracker.story import parse
import logging

PROJECTS_URL    = 'https://www.pivotaltracker.com/services/v3/projects'
STORIES_URL     = 'https://www.pivotaltracker.com/services/v3/projects/{0}/stories'
STORY_URL       = 'https://www.pivotaltracker.com/services/v3/projects/{0}/stories/{1}'

def _get_data(guid, url_pattern, parameters):
    url = url_pattern.format(*parameters)
    data = requests.get(url, headers={'X-TrackerToken': guid})
    if not data.status_code == 200:
        print(url, data.status_code, data.content)
        raise Exception(data.content)
    return data.content
    
def projects(guid):
    xml = _get_data(guid, PROJECTS_URL, ())

    xml = etree.parse(StringIO.StringIO(xml))
    
    for project in xml.findall('project'):
        print("Project {0}: {1}".format(project.find('name').text, project.find('id').text))

def stories(guid, project_id):
    url = STORIES_URL.format(project_id)
    data = requests.get(url, headers={'X-TrackerToken': guid})
    if not data.status_code == 200:
        print(data.status_code, data.content)
        return 1

    xml = etree.parse(StringIO.StringIO(data.content))
    import pdb;pdb.set_trace()
    print(xml)

def story(guid, project_id, story_id):
    story = parse(_get_data(guid, STORY_URL, (project_id, story_id)))

    print("{0} {1} - {2}".format(story.story_type, story.id, story.name))
    print("Labels: {0}".format(story.labels))
    print("Status: {0}".format(story.current_state))
    print("Created: {0}".format(story.created_at))
    print("Updated: {0}".format(story.updated_at))
    print("Accepted: {0}".format(story.accepted_at))
    print("Requested by: {0}".format(story.requested_by))
    print("Owned by: {0}".format(story.owned_by))
    print("URL: {0}".format(story.url))
    print(story.description)
    for note in story.notes:
        print("\n")
        print("{0} - {1}".format(note.author, note.noted_at))
        print('"{0}"'.format(note.text))
