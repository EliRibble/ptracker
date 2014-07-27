import StringIO
from ptracker import remote
from ptracker import db, types, synchronizer
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
    db.init(db_user, db_password, db_name)
    synchronizer.sync_all(guid, db_user, db_password, db_name)
    return 0

def projects(guid):
    projects = remote.get_projects(guid)
    for project in projects:
        print("Project {0}: {1}".format(project.name, project.id))

def stories(guid, project_id):
    stories = remote.get_stories(guid, project_id)
    logging.info("%s stories", len(stories))

def story(guid, project_id, story_id):
    story = remote.get_story(guid, project_id, story_id)
    import pdb;pdb.set_trace()
    print(story)


def activities(guid, story_id):
    activities = remote.get_activities(guid, story_id)
    for activity in activities:
        logging.info("Activity {0} ({1}) - {2}".format(activity.id, activity.version, activity.event_type))
        #logging.info("Author: {0}".format(activity.author))
        logging.info("Occurred: {0}".format(activity.occurred_at))
        logging.info("Description: {0}".format(activity.description))
