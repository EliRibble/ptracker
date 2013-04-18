import StringIO
from lxml import etree
from sqlalchemy import Integer, String, DateTime, Boolean, Column, Table, ForeignKey, Text
from sqlalchemy.orm import relationship, backref
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

project_labels = Table('project_labels', Base.metadata,
    Column('project_id', String(20), ForeignKey('projects.id')),
    Column('label', String(200), ForeignKey('labels.name')))

story_labels = Table('story_labels', Base.metadata,
    Column('story_id', String(20), ForeignKey('stories.id')),
    Column('label', String(200), ForeignKey('labels.name')))

project_members = Table('project_members', Base.metadata,
    Column('project_id', String(20), ForeignKey('projects.id')),
    Column('user_id', String(20), ForeignKey('users.id')))

class Story(Base):
    __tablename__ = 'stories'
    id              = Column(String(20), primary_key=True)
    project_id      = Column(String(20))
    story_type      = Column(String(20))
    url             = Column(String(512))
    current_state   = Column(String(20))
    description     = Column(Text())
    name            = Column(Text())
    requested_by_id = Column(String(20), ForeignKey('users.id'))
    owned_by_id     = Column(String(20), ForeignKey('users.id'))

    requested_by    = relationship("User", backref='requested_stories', foreign_keys=[requested_by_id])
    owned_by        = relationship("User", backref='owned_stories', foreign_keys=[owned_by_id])
    
    created_at      = Column(DateTime())
    updated_at      = Column(DateTime())
    accepted_at     = Column(DateTime())
    labels          = relationship("Label", secondary=story_labels, backref='stories')
    
class Note(Base):
    __tablename__ = 'notes'
    id          = Column(String(20), primary_key=True)
    text        = Column(Text())
    noted_at    = Column(DateTime())
    author_id   = Column(String(20), ForeignKey('users.id'))
    story_id    = Column(String(20), ForeignKey('stories.id'))
    author      = relationship("User", backref='notes')
    story       = relationship("Story", backref='notes')
 
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
    def __repr__(self):
        return u"Label '{0}'".format(self.name)

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

