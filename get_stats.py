#!/usr/bin/env python
import sys

try:
    import settings
except ImportError:
    print("Please create a settings.py from the settings.py.template")
    sys.exit(1)

from objects import Project
import urllib2
import base64
from lxml import etree
LOGIN_URL = 'https://www.pivotaltracker.com/services/v3/tokens/active'
PROJECTS_URL = 'https://www.pivotaltracker.com/services/v3/projects'
STORIES_URL = 'https://www.pivotaltracker.com/services/v3/projects/{0}/stories'

def get_guid():
    password_manager = urllib2.HTTPPasswordMgrWithDefaultRealm()
    password_manager.add_password(None, LOGIN_URL, settings.username, settings.password)
    auth_handler = urllib2.HTTPBasicAuthHandler(password_manager)
    opener = urllib2.build_opener(auth_handler)
    urllib2.install_opener(opener)

    data = etree.parse(urllib2.urlopen(LOGIN_URL))
    guid = data.find('guid').text
    return guid

def get_projects():
    req = urllib2.Request(PROJECTS_URL)
    req.add_header('X-TrackerToken', settings.guid)
    data = etree.parse(urllib2.urlopen(req))
    projects = []
    for project in data.findall('project'):
        projects.append(Project(project))
    return projects

def get_bugs():
    pass
    
def main():
    #guid = get_guid()
    #get_bugs()
    projects = get_projects()
    for p in projects:
        print("{0}: {1} members, {2} bugs".format(p, len(p.members), len(p.bugs())))
        p.bugs()


if __name__ == '__main__':
    main()
