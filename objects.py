import settings
import pivotal
import urllib

class PivotalObject(object):
    def __init__(self, xml):
        for f in self.FIELDS:
            item = xml.find(f)
            if item is not None and item.text:
                setattr( self, f, item.text )
            else:
                setattr( self, f, None )


class Project(PivotalObject):
    FIELDS = ['id',
        'name',
        'iteration_length',
        'week_start_day',
        'point_scale',
        'account', 
        'first_iteration_start_time',
        'current_iteration_number',
        'enable_tasks',
        'velocity_scheme',
        'current_velocity',
        'initial_velocity',
        'number_of_done_iterations_to_show',
        'labels',
        'last_activity_at',
        'allow_attachments',
        'public',
        'use_https',
        'bugs_and_chores_are_estimatable',
        'commit_mode']

    def __init__(self, xml):
        super(Project, self).__init__(xml)

        self._parse_members(xml.find('memberships'))
        self._bugs = []
        
    def __str__(self):
        return "Project {0}-{1}".format(self.id, self.name)

    def _parse_members(self, xml):
        self.members = []
        for membership in xml.findall('membership'):
            self.members.append(Member(membership))
        
    def bugs(self):
        if not self._bugs:
            self._bugs = self._get_bugs()
        return self._bugs

    def _get_bugs(self):
        BUGS_URL = 'https://www.pivotaltracker.com/services/v3/projects/{0}/stories?{1}'
        formatted_url = BUGS_URL.format(self.id, urllib.urlencode({"filter": "type:bug"}))
        req = pivotal.get_url(formatted_url, settings.guid)
        return self._parse_stories(req)
        
    def _parse_stories(self, data):
        stories = []
        for bug in data.findall('story'):
            stories.append(Story(bug))   
        return stories
        
            

class Member(PivotalObject):
    FIELDS = [
        'id',
        'role'
    ]

    PERSON_FIELDS = [
        'email',
        'name',
        'initials'
    ]

    def __init__(self, xml):
        super(Member, self).__init__(xml)
 
        person = xml.find('person')
        for f in Member.PERSON_FIELDS:
            setattr(self, f, person.find(f).text)
        

class Story(PivotalObject):
    FIELDS = [
        'id',
        'project_id',
        'story_type',
        'url',
        'current_state',
        'description',
        'name',
        'requested_by',
        'created_at',
        'updated_at',
        'labels',
    ]
    
    def __init__(self, xml):
        super(Story, self).__init__(xml)
