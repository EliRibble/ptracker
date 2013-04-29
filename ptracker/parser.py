import StringIO
from lxml import etree
       
class ParsedThing(object):
    def __init__(self, t):
        self.type = t

    def __repr__(self):
        return u'Parsed {0}'.format(self.type)

def _parse_note(note):
    n = ParsedThing('note')
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
    s = ParsedThing('story')
    s.id            = story.find('id').text
    s.project_id    = story.find('project_id').text
    s.story_type    = story.find('story_type').text
    s.url           = story.find('url').text
    s.current_state = story.find('current_state').text
    description     = story.find('description')
    s.description   = description.text if description is not None else None
    s.name          = story.find('name').text
    s.requested_by  = story.find('requested_by').text
    s.created_at    = story.find('created_at').text
    owned_by        = story.find('owned_by')
    s.owned_by      = owned_by.text if owned_by is not None else None
    accepted_at     = story.find('accepted_at')
    s.accepted_at   = accepted_at.text if accepted_at is not None else None
    notes           = story.find('notes')
    s.notes         = _parse_notes(notes) if notes is not None else []
    labels          = story.find('labels')
    s.labels        = labels.text.split(',') if labels is not None else []
    return s

def _parse_stories(xml):
    stories = []
    for story in xml:
        stories.append(_parse_story(story))
    return stories
 
def _parse_activity(activity):
    a = ParsedThing('activity')
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

def _parse_member(member):
    m = ParsedThing('member')
    m.id = member.find('id').text
    person = member.find('person')
    m.email = person.find('email').text
    m.name = person.find('name').text
    m.initials = person.find('initials').text
    return m
   
def _parse_project(project):
    p = ParsedThing('project')
    p.id                                = project.find('id').text
    p.name                              = project.find('name').text
    p.iteration_length                  = project.find('iteration_length').text
    p.week_start_day                    = project.find('week_start_day').text
    p.point_scale                       = project.find('point_scale').text
    p.account                           = project.find('account').text
    p.first_iteration_start_time        = project.find('first_iteration_start_time').text
    p.current_iteration_number          = project.find('current_iteration_number').text
    p.enable_tasks                      = project.find('enable_tasks').text
    p.velocity_scheme                   = project.find('velocity_scheme').text
    p.current_velocity                  = project.find('current_velocity').text
    p.initial_velocity                  = project.find('initial_velocity').text
    p.number_of_done_iterations_to_show = project.find('number_of_done_iterations_to_show').text
    p.last_activity_at                  = project.find('last_activity_at').text
    p.allow_attachments                 = project.find('allow_attachments').text
    p.public                            = project.find('public').text
    p.use_https                         = project.find('use_https').text
    p.bugs_and_chores_are_estimatable   = project.find('bugs_and_chores_are_estimatable').text
    p.commit_mode                       = project.find('commit_mode').text
    
    p.members = [_parse_member(m) for m in project.find('memberships')]

    labels = project.find('labels').text
    if labels:
        p.labels  = labels.split(',')
    else:
        p.labels = []
    return p
    
def _parse_projects(xml):
    projects = []
    for project in xml:
        projects.append(_parse_project(project))
    return projects

def parse(xml):
    xml = etree.parse(StringIO.StringIO(xml))
    if xml.getroot().tag == 'projects':
        return _parse_projects(xml.getroot())
    elif xml.getroot().tag == 'stories':
        return _parse_stories(xml.getroot())
    elif xml.getroot().tag == 'story':
        return _parse_story(xml.getroot())
    elif xml.getroot().tag == 'activities':
        return _parse_activities(xml.getroot())

def has_story_creation(xml):
    root = etree.parse(StringIO.StringIO(xml)).getroot()
    for activity in root:
        if activity.find('event_type').text == 'story_create':
            return True
    return False
