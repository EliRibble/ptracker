import StringIO
from lxml import etree

class Story(object):
    def __init__(self):
        self.id            = None
        self.project_id    = None
        self.story_type    = None
        self.url           = None
        self.current_state = None
        self.description   = None
        self.name          = None
        self.requested_by  = None
        self.owned_by      = None
        self.created_at    = None
        self.updated_at    = None
        self.accepted_at   = None
        self.labels        = None
        self.notes         = []
    
class Note(object):
    def __init__(self):
        self.id        = None
        self.text      = None
        self.author    = None
        self.noted_at  = None
        
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

def parse(xml):
    xml = etree.parse(StringIO.StringIO(xml))
    if xml.getroot().tag == 'story':
        return _parse_story(xml.getroot())
