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
 
class Activity(object):
    pass

class Project(object):
    pass

class User(object):
    pass
