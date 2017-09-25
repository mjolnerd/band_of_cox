#!/usr/bin/env python
'''
Shamelessly stolen from https://gist.github.com/yosemitebandit/1805918
Going to use this as a base for scraping current Bandwidth usage from
cox.net.
'''
import sys
import requests
from BeautifulSoup import BeautifulSoup

# need to capture a valid csrf token
# first visit the login page to generate one
s = requests.session()
response = s.get('https://www.cox.com/resaccount/sign-in.cox')
'''
# extract the token
soup = BeautifulSoup(response.text)
for n in soup('input'):
    if n['name'] == '_csrf_token':
        token = n['value']
        break
'''
try:
    from creds import *
except ImportError:
    sys.exit()
# now post to that login page with some valid credentials and the token
auth = {
    'targetFN': 'COX.net'
    ,'emaildomain': '@cox.net'
    ,'username': coxuser
    ,'password': coxpass
    ,'signin-submit': 'Sign In'
    ,'onsuccess': 'https%3A%2F%2Fwww.cox.com%2Fresaccount%2Fhome.cox'
    ,'onfailure': 'http://www.cox.com/resaccount/sign-in.cox?onsuccess=https%3A%2F%2Fwww.cox.com%2Fresaccount%2Fhome.cox'
}
print auth
s.post('https://idm.east.cox.net/idm/coxnetlogin', data=auth)

# now we should be authenticated, try visiting a protected page
response = s.get('https://www.cox.com/internet/mydatausage.cox')
print response.text
