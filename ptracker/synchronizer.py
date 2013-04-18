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
