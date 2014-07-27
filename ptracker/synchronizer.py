import logging
from ptracker import remote, db, types
from sqlalchemy import exc

LOGGER = logging.getLogger('sync')

def _to_orm(parsed, orm_type, overrides=None):
    orm = orm_type()
    overrides = [] if overrides is None else overrides
    for k, v in parsed.__dict__.items():
        if k in overrides:
            setattr(orm, k, overrides[k])
        else:
            try:
                setattr(orm, k, v)
            except:
                print("Bad time setting {0} to {1}".format(k, v))
                raise
    return orm

def sync_all(guid, db_user, db_password, db_name):
    session = db.Session()
    projects = remote.get_projects(guid)
    LOGGER.info('Scanning %d projects', len(projects))
    for project in projects:
        LOGGER.info("Scanning project %d", project.id)
        for user in project.members:
            db_user = _to_orm(user, types.User)
            db_user = session.merge(db_user)
        for label in project.labels:
            db_label = types.Label()
            db_label.name = label
            db_label = session.merge(db_label)
        db_project = _to_orm(project, types.Project, {'labels':[], 'members':[]})
        db_project = session.merge(db_project)
    
        member_names = [m.name for m in project.members] 
        db_project.members = list(session.query(types.User).filter(types.User.name.in_(member_names)))
        
        db_project.labels = list(session.query(types.Label).filter(types.Label.name.in_(project.labels)))

        session.commit()
    for project in projects:
        _sync_stories(guid, project, session)
    session.commit()

def _sync_stories(guid, project, session):
    stories = remote.get_stories(guid, project.id)
    LOGGER.info("Scanning %d stories", len(stories))
    for story in stories:
        db_story = _to_orm(story, types.Story, {'requested_by': None, 'owned_by': None, 'labels': [], 'notes': []})
        try:
            db_story = session.merge(db_story)
        except exc.IntegrityError, e:
            LOGGER.error("Failed to save story %d: %s", story.id, e)
            session.rollback()
            continue
        db_story.labels = list(session.query(types.Label).filter(types.Label.name.in_(story.labels)))
        try:
            db_story.requested_by = session.query(types.User).filter(types.User.name==story.requested_by)[0]
        except IndexError:
            db_requested_by = types.User(name=story.requested_by)
            session.add(db_requested_by)
            db_story.requested_by = db_requested_by
        if story.owned_by:
            try:
                db_story.owned_by = session.query(types.User).filter(types.User.name==story.owned_by)[0]
            except IndexError:
                db_owned_by = types.User(name=story.owned_by)
                session.add(db_owned_by)
                db_story.owned_by = db_owned_by
        activities = remote.get_activities(guid, story.id)
        LOGGER.info("Scanning %d activities", len(activities))
        for activity in activities:
            db_activity = _to_orm(activity, types.Activity)
            try:
                db_activity = session.merge(db_activity)
            except exc.IntegrityError, e:
                LOGGER.error("Failed to save activity %d: %s", activity.id, e)
                session.rollback()
