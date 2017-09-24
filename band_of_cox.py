#!/usr/bin/env python
'''
Shamelessly stolen from https://gist.github.com/yosemitebandit/1805918
Going to use this as a base for scraping current Bandwidth usage from
cox.net.
'''
import requests
from BeautifulSoup import BeautifulSoup

# need to capture a valid csrf token
# first visit the login page to generate one
s = requests.session()
response = s.get('https://callmeduele.com/login')

# extract the token
soup = BeautifulSoup(response.text)
for n in soup('input'):
    if n['name'] == '_csrf_token':
        token = n['value']
        break

# now post to that login page with some valid credentials and the token
auth = {
    'userName': 'batman'
    , 'password': 'j0kersuck5'
    , '_csrf_token': token
}
s.post('https://callmeduele.com/login', data=auth)

# now we should be authenticated, try visiting a protected page
response = s.get('https://callmeduele.com/cases')
print response.text
