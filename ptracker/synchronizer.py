from ptracker import remote, db, types

def _to_orm(parsed, orm_type, overrides=None):
    orm = orm_type()
    overrides = [] if overrides is None else overrides
    for k, v in parsed.__dict__.items():
        if k in overrides:
            setattr(orm, k, overrides[k])
        else:
            setattr(orm, k, v)
    return orm

def sync_all(guid, db_user, db_password, db_name):
    session = db.Session()
    projects = remote.get_projects(guid)
    for project in projects:
        for user in project.members:
            db_user = _to_orm(user, types.User)
            db_user = session.merge(db_user)
        for label in project.labels:
            db_label = types.Label()
            db_label.name = label
            db_label = session.merge(db_label)
        db_project = _to_orm(project, types.Project, {'labels':[], 'members':[]})
        db_project = session.merge(db_project)
    
        member_ids = [m.id for m in project.members] 
        db_project.members = list(session.query(types.User).filter(types.User.id.in_(member_ids)))
        
        db_project.labels = list(session.query(types.Label).filter(types.Label.name.in_(project.labels)))

        session.commit()
        _sync_stories(guid, project, session)
    session.commit()

def _sync_stories(guid, project, session):
    stories = remote.get_stories(guid, project.id)
    for story in stories:
        db_story = _to_orm(story, types.Story, {'requested_by': None, 'owned_by': None, 'labels': [], 'notes': []})
        db_story = session.merge(db_story)
        db_story.labels = list(session.query(types.Label).filter(types.Label.name.in_(story.labels)))
        try:
            db_story.requested_by = session.query(types.User).filter(types.User.name==story.requested_by)[0]
        except IndexError:
            db_requested_by = types.User(id=story.requested_by, name=story.requested_by)
            session.add(db_requested_by)
            db_story.requested_by = db_requested_by
        if story.owned_by:
            try:
                db_story.owned_by = session.query(types.User).filter(types.User.name==story.owned_by)[0]
            except IndexError:
                db_owned_by = types.User(id=story.owned_by, name=story.owned_by)
                session.add(db_owned_by)
                db_story.owned_by = db_owned_by
