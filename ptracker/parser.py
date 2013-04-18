import StringIO
from lxml import etree
from ptracker.types import Story, Note, Activity
       
def _parse_note(note):
    n = Note()
    n.id        = note.find('id').text
    n.text      = note.find('text').text
    n.author    = note.find('author').text
    n.noted_at  = note.find('noted_at').text
    return n

def _parse_notes(notes):
    note_objs = []
    for note in notes:
        note_objs.append(_parse_note(note))
    return note_objs

def _parse_story(story):
    s = Story()
    s.id            = story.find('id').text
    s.project_id    = story.find('project_id').text
    s.story_type    = story.find('story_type').text
    s.url           = story.find('url').text
    s.current_state = story.find('current_state').text
    s.description   = story.find('description').text
    s.name          = story.find('name').text
    s.requested_by  = story.find('requested_by').text
    s.owned_by      = story.find('owned_by').text
    s.created_at    = story.find('created_at').text
    s.updated_at    = story.find('updated_at').text
    s.accepted_at   = story.find('accepted_at').text
    s.labels        = story.find('labels').text
    s.notes         = _parse_notes(story.find('notes'))
    return s

def _parse_stories(xml):
    stories = []
    for story in xml:
        stories.append(_parse_story(story))
    return stories
 
def _parse_activity(activity):
    a = Activity()
    a.id            = activity.find('id').text
    a.version       = activity.find('version').text
    a.event_type    = activity.find('event_type').text
    a.occurred_at   = activity.find('occurred_at').text
    a.project_id    = activity.find('project_id').text
    a.description   = activity.find('description').text
    a.author        = activity.find('author').text
    if a.author.strip() == '':
        a.author = None
    for subnode in activity:
        if subnode.text.strip() != '':
            print("{0}: {1}".format(subnode.tag, subnode.text))
        else:
            if subnode.tag == 'stories':
                for story in subnode:
                    for subsubnode in story:
                        print("\t{0}: {1}".format(subsubnode.tag, subsubnode.text))
    print("-------")
    return a

def _parse_activities(xml):
    activities = []
    for activity in xml:
        activities.append(_parse_activity(activity))
    return activities

def parse(xml):
    xml = etree.parse(StringIO.StringIO(xml))
    if xml.getroot().tag == 'stories':
        return _parse_stories(xml.getroot())
    elif xml.getroot().tag == 'story':
        return _parse_story(xml.getroot())
    elif xml.getroot().tag == 'activities':
        return _parse_activities(xml.getroot())
