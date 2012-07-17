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
        
    def __str__(self):
        return "Project {0}-{1}".format(self.id, self.name)
        
