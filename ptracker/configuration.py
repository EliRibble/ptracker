import os
import ConfigParser
import copy
import logging

_configuration = {}

OPTIONS = {
    'guid': None,
    'project_id': None
}

def initialize(args):
    global _configuration
    _configuration = copy.copy(OPTIONS)

    config_file = os.path.abspath(os.path.join(os.environ['HOME'], '.ptracker'))
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
