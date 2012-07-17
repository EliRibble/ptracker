class Project():
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
        for f in Project.FIELDS:
            setattr(self, f, xml.find(f).text)

        self._parse_members(xml.find('memberships'))
        
    def __str__(self):
        return "Project {0}-{1}".format(self.id, self.name)

    def _parse_members(self, xml):
        self.members = []
        for membership in xml.findall('membership'):
            self.members.append(Member(membership))
        

class Member():
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
        for f in Member.FIELDS:
            setattr(self, f, xml.find(f).text)
 
        person = xml.find('person')
        for f in Member.PERSON_FIELDS:
            setattr(self, f, person.find(f).text)
        
