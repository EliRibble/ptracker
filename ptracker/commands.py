import requests
from lxml import etree
import StringIO

PROJECTS_URL = 'https://www.pivotaltracker.com/services/v3/projects'

def projects(guid):
    data = requests.get(PROJECTS_URL, headers={'X-TrackerToken': guid})
    assert data.status_code == 200
    xml = etree.parse(StringIO.StringIO(data.content))
    
    #import pdb;pdb.set_trace()
    for project in xml.findall('project'):
        print("Project {0}: {1}".format(project.find('name').text, project.find('id').text))

