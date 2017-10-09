#!/usr/bin/env python
'''
Shamelessly stolen from https://gist.github.com/yosemitebandit/1805918
Going to use this as a base for scraping current Bandwidth usage from
cox.net.
'''
import sys
import requests
import json
from datetime import datetime
from bs4 import BeautifulSoup
from elasticsearch import Elasticsearch

# We are going to store our results in Elasticsearch.
es = Elasticsearch([{'host': 'localhost', 'port': 9200}])

# Set up a session for our pull from Cox
s = requests.session()

# The creds file holds a plaintext username/password for the cox.net account.
#  Plaintext is naughty.  Only run this on hosts which are adequately secured.
#  Secrets management is "hard".  May tackle this with something better later.
try:
    from creds import *
except ImportError:
    sys.exit()
# post to the login page with some valid credential
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
json_ext = json.loads(script.text.replace('var utag_data=','').replace('[','').replace(']',''))

'''
Map this using:
PUT coxnet
{
  "mappings": {
    "utag_data":{
      "properties": {
        "dateStamp":{
          "type": "date",
          "format": "epoch_second"
        },
        "dumDaysLeft":{
          "type": "short"
        },
        "dumDaysLimit":{
          "type": "short"
        },
        "dumUsage":{
          "type": "short"
        },
        "dumUtilization":{
          "type": "short"
        }
      }
    }
  }
}
'''

# Now we have a nice shiny JSON object.  Lets stuff it into Elasticsearch for long term storage.
es.index(index='coxnet', doc_type='utag_data', body=json_ext)
