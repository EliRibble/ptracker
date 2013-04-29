import os
import ConfigParser
import copy
import logging

_configuration = {}

OPTIONS = {
    'guid'          : None,
    'project_id'    : None,
    'db_user'       : None,
    'db_password'   : None,
    'db_name'       : None
}

def initialize(args):
    global _configuration
    _configuration = copy.copy(OPTIONS)

    ptracker_home = os.path.abspath(os.path.join(os.environ['HOME'], '.ptracker'))
    if not os.path.exists(ptracker_home):
        try:
            os.mkdir(ptracker_home)
        except IOError, ex:
            logging.error("Unable to create ptracker home at %s", ptracker_home)
            return

    config_file = os.path.abspath(os.path.join(os.environ['HOME'], '.ptracker', 'config'))
    try:
        config = ConfigParser.SafeConfigParser()
        config.read(config_file)
        for k, v in OPTIONS.items():
            if config.has_option('ptracker', k):
                _configuration[k] = config.get('ptracker', k)
    except IOError, ex:
        logging.info("Unable to read ptracker config file: %s", ex)

        
def get(key):
    return _configuration[key]
