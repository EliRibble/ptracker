import StringIO
from lxml import etree
from sqlalchemy import BigInteger, Integer, String, DateTime, Boolean, Column, Table, ForeignKey, Text
from sqlalchemy.orm import relationship, backref
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

project_label = Table('project_label', Base.metadata,
    Column('project_id', BigInteger(), ForeignKey('project.id')),
    Column('label', String(200), ForeignKey('label.name')))

story_label = Table('story_label', Base.metadata,
    Column('story_id', BigInteger(), ForeignKey('story.id')),
    Column('label', String(200), ForeignKey('label.name')))

project_members = Table('project_members', Base.metadata,
    Column('project_id', BigInteger(), ForeignKey('project.id')),
    Column('user_id', BigInteger(), ForeignKey('user.id')))

story_activity = Table('story_activity', Base.metadata,
    Column('activity_id', BigInteger(), ForeignKey('activity.id')),
    Column('story_id', BigInteger(), ForeignKey('story.id')))

class Story(Base):
    __tablename__ = 'story'
    id              = Column(BigInteger(), primary_key=True)
    project_id      = Column(String(20))
    story_type      = Column(String(20))
    url             = Column(String(512))
    current_state   = Column(String(20))
    description     = Column(Text())
    name            = Column(Text())
    requested_by_id = Column(BigInteger(), ForeignKey('user.id'))
    owned_by_id     = Column(BigInteger(), ForeignKey('user.id'))

    requested_by    = relationship("User", backref='requested_story', foreign_keys=[requested_by_id])
    owned_by        = relationship("User", backref='owned_story', foreign_keys=[owned_by_id])
    
    created_at      = Column(DateTime())
    updated_at      = Column(DateTime())
    accepted_at     = Column(DateTime())
    label           = relationship("Label", secondary=story_label, backref='story')
    activity        = relationship("Activity", secondary=story_activity, backref='story')
    
class Note(Base):
    __tablename__ = 'note'
    id          = Column(BigInteger(), primary_key=True)
    text        = Column(Text())
    noted_at    = Column(DateTime())
    author_id   = Column(BigInteger(), ForeignKey('user.id'))
    story_id    = Column(BigInteger(), ForeignKey('story.id'))
    author      = relationship("User", backref='note')
    story       = relationship("Story", backref='note')
 
class Activity(Base):
    __tablename__ = 'activity'
    id          = Column(BigInteger(), primary_key=True)
    version     = Column(Integer())
    event_type  = Column(String(100))
    ocurred_at  = Column(DateTime())
    author_id   = Column(BigInteger(), ForeignKey('user.id'))
    project_id  = Column(BigInteger(), ForeignKey('project.id'))

    author      = relationship("User", backref='activities_authored', foreign_keys=[author_id])
    project     = relationship("Project", backref='activities', foreign_keys=[project_id])

    description = Column(Text())

class User(Base):
    __tablename__ = 'user'
    id          = Column(BigInteger(), primary_key=True)
    name        = Column(String(200))
    email       = Column(String(200))
    initials    = Column(String(3))
    def __init__(self, name=None, email=None, initials=None):
        self.name       = name
        self.email      = email
        self.initials   = initials if initials else (''.join([n.upper()[0] for n in name.split()]) if name else None)

class Label(Base):
    __tablename__ = 'label'
    name    = Column(String(200), primary_key=True)
    def __repr__(self):
        return u"Label '{0}'".format(self.name)

class Project(Base):
    __tablename__ = 'project'
    id                                  = Column(BigInteger(), primary_key=True)
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
    label                               = relationship("Label", secondary=project_label, backref='project')
    members                             = relationship("User", secondary=project_members, backref='project')

