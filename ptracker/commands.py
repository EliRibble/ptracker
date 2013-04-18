import StringIO
from ptracker import remote
from ptracker import db, types
import logging

def setupdb(db_user, db_password, db_name):
    try:
        db.init(db_user, db_password, db_name)
        db.setupdb()
        return 0
    except Exception, e:
        print(e)
        return 1
    
def sync(guid, db_user, db_password, db_name):
    projects = remote.get_projects(guid)
    db.init(db_user, db_password, db_name)
    session = db.Session()
    labels = set()
    existing_labels = {}
    for project in projects:
        for label in project.labels:
            labels.add(label.name)
    for label in labels:
        existing_labels[label] = session.merge(types.Label(label))
    session.commit()
    for project in projects:
        project.labels = [existing_labels[label.name] for label in project.labels]
        session.add(project)
    session.commit()

def projects(guid):
    projects = remote.get_projects(guid)
    for project in projects:
        print("Project {0}: {1}".format(project.name, project.id))

def stories(guid, project_id):
    stories = remote.get_stories(guid, project_id)
    logging.info("%s stories", len(stories))

def story(guid, project_id, story_id):
    story = remote.get_story(guid, project_id, story_id)

    print("{0} {1} - {2}".format(story.story_type, story.id, story.name))
    print("Labels: {0}".format(story.labels))
    print("Status: {0}".format(story.current_state))
    print("Created: {0}".format(story.created_at))
    print("Updated: {0}".format(story.updated_at))
    print("Accepted: {0}".format(story.accepted_at))
    print("Requested by: {0}".format(story.requested_by))
    print("Owned by: {0}".format(story.owned_by))
    print("URL: {0}".format(story.url))
    print(story.description)
    for note in story.notes:
        print("\n")
        print("{0} - {1}".format(note.author, note.noted_at))
        print('"{0}"'.format(note.text))

def activities(guid, story_id):
    activities = remote.get_activities(guid, story_id)
    for activity in activities:
        logging.info("Activity {0} ({1}) - {2}".format(activity.id, activity.version, activity.event_type))
        #logging.info("Author: {0}".format(activity.author))
        logging.info("Occurred: {0}".format(activity.occurred_at))
        logging.info("Description: {0}".format(activity.description))
