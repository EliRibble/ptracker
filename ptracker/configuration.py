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

PTRACKER_HOME = os.path.abspath(os.path.join(os.environ['HOME'], '.ptracker'))
def initialize(args):
    global _configuration
    _configuration = copy.copy(OPTIONS)

    if not os.path.exists(PTRACKER_HOME):
        try:
            os.mkdir(PTRACKER_HOME)
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
