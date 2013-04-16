import requests
from lxml import etree
import StringIO
from ptracker.story import parse
import logging

PROJECTS_URL    = 'https://www.pivotaltracker.com/services/v3/projects'
STORIES_URL     = 'https://www.pivotaltracker.com/services/v3/projects/{0}/stories'
STORY_URL       = 'https://www.pivotaltracker.com/services/v3/projects/{0}/stories/{1}'

ACTIVITIES_URL  = 'https://www.pivotaltracker.com/services/v4/stories/{0}/activities?limit=100'

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
    stories = parse(_get_data(guid, STORIES_URL, (project_id,)))
    logging.info("%s stories", len(stories))

def story(guid, project_id, story_id):
    if not story_id:
        raise Exception("You must specify a story id")

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

def activities(guid, story_id):
    if not story_id:
        raise Exception("You must specify a story id")

    activities = parse(_get_data(guid, ACTIVITIES_URL, (story_id,)))
    for activity in activities:
        logging.info("Activity {0} ({1}) - {2}".format(activity.id, activity.version, activity.event_type))
        #logging.info("Author: {0}".format(activity.author))
        logging.info("Occurred: {0}".format(activity.occurred_at))
        logging.info("Description: {0}".format(activity.description))
