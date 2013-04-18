import StringIO
from lxml import etree
from sqlalchemy import Integer, String, DateTime, Boolean, Column, Table, ForeignKey
from sqlalchemy.orm import relationship, backref
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

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

class User(Base):
    __tablename__ = 'users'
    id          = Column(String(20), primary_key=True)
    name        = Column(String(200))
    email       = Column(String(200))
    initials    = Column(String(3))


class Label(Base):
    __tablename__ = 'labels'
    name    = Column(String(200), primary_key=True)

project_labels = Table('project_labels', Base.metadata,
    Column('project_id', String(20), ForeignKey('projects.id')),
    Column('tag', String(20), ForeignKey('labels.name')))

project_members = Table('project_members', Base.metadata,
    Column('project_id', String(20), ForeignKey('projects.id')),
    Column('user_id', String(20), ForeignKey('users.id')))

class Project(Base):
    __tablename__ = 'projects'
    id                                  = Column(String(20), primary_key=True)
    name                                = Column(String(200))
    iteration_length                    = Column(Integer())
    week_start_day                      = Column(String(10))
    point_scale                         = Column(String(20))
    account                             = Column(String(200))
    first_iteration_start_time          = Column(DateTime())
    current_iteration_number            = Column(Integer())
    enabled_tasks                       = Column(Boolean())
    velocity_scheme                     = Column(String(200))
    current_velocity                    = Column(Integer())
    initial_velocity                    = Column(Integer())
    number_of_done_iterations_to_show   = Column(Integer())
    last_activity_at                    = Column(DateTime())
    allow_attachments                   = Column(Boolean())
    public                              = Column(Boolean())
    use_https                           = Column(Boolean())
    bugs_and_chores_are_estimatable     = Column(Boolean())
    commit_mode                         = Column(Boolean())
    labels                              = relationship("Label", secondary=project_labels, backref='projects')
    members                             = relationship("User", secondary=project_members, backref='projects')

