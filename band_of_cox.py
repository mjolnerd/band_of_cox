#!/usr/bin/env python
'''
Shamelessly stolen from https://gist.github.com/yosemitebandit/1805918
Going to use this as a base for scraping current Bandwidth usage from
cox.net.
'''
import sys
import requests
import re
from bs4 import BeautifulSoup

# need to capture a valid csrf token
# first visit the login page to generate one
s = requests.session()
response = s.get('https://www.cox.com/resaccount/sign-in.cox')

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
s.post('https://idm.east.cox.net/idm/coxnetlogin', data=auth)

# now we should be authenticated, try visiting a protected page
response = s.get('https://www.cox.com/internet/mydatausage.cox')
soup = BeautifulSoup(response.text, "html.parser")
# Looks like the utag data is in the second JS on this page
script = soup.find_all('script')[1]

utag = {}
# Example:
#     "dateStamp": "1506819104",
#
# This isn't terribly robust or elegant.  Might be worth swapping in
#  https://github.com/rspivak/slimit at some point. This is ok for now though.
for line in script.text.splitlines():
    if ':' in line:
        line = line.strip()
        line = line.replace('"','')
        line = line.replace(',','')
        fkey = line.split(':')[0].strip()
        fval = line.split(':')[1].strip()
        utag[fkey] = fval

# Now we have a dict with all the data in utag.  Can probably do something useful with that.
#  Let's just print Data Usage Meter out for now.
dumstuff = ['dumUsage','dumLimit','dumDaysLeft','dumUtilization']
for dum in dumstuff:
    print "%s %s" % (dum, utag[dum])
