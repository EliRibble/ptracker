#!/usr/bin/env python
import sys

try:
    import settings
except ImportError:
    print("Please create a settings.py from the settings.py.template")
    sys.exit(1)

import urllib2
import base64

LOGIN_URL = 'https://www.pivotaltracker.com/services/v3/tokens/active'

def get_guid():
    password_manager = urllib2.HTTPPasswordMgrWithDefaultRealm()
    password_manager.add_password(None, LOGIN_URL, settings.username, settings.password)
    auth_handler = urllib2.HTTPBasicAuthHandler(password_manager)
    opener = urllib2.build_opener(auth_handler)
    urllib2.install_opener(opener)

    handle = urllib2.urlopen(LOGIN_URL)
    print(handle.read())
        
    
def main():
    guid = get_guid()


if __name__ == '__main__':
    main()
