from google.appengine.api import urlfetch

import os
import webapp2
import jinja2
import json
import logging
import string
import random
import httplib
import urllib
 
jinja_environment = jinja2.Environment(autoescape=True, loader=jinja2.FileSystemLoader(os.path.join(os.path.dirname(__file__), 'templates')))
GOOGLE_SERVER = "https://accounts.google.com/o/oauth2/v2/auth"

CLIENT_ID="1075487943853-i6t2ua56n8oo8960cmkhu7tona5u9bh9.apps.googleusercontent.com"
CLIENT_SECRET = "JcIf1764iYwahLxT9P5GBBYa"
REDIRECT_URI = "https://oauth2-166722.appspot.com"
#REDIRECT_URI = "http://localhost:8080"

TOKEN_URL = "https://www.googleapis.com/oauth2/v4/token"
GPLUS_URL = "https://www.googleapis.com/plus/v1/people/me"


def id_generator(size=12, chars=string.ascii_uppercase + string.digits):
	return ''.join(random.choice(chars) for _ in range(size))


def request_token(self, code):
	headers = {'Content-Type': 'application/x-www-form-urlencoded'}
	payload = { \
		'code': code, \
		'client_id': CLIENT_ID, \
		'client_secret': CLIENT_SECRET, \
		'redirect_uri': REDIRECT_URI, \
		'grant_type': 'authorization_code'
	}
	encoded_data = urllib.urlencode(payload)
	result = urlfetch.fetch(url=TOKEN_URL, payload=encoded_data, method=urlfetch.POST, headers=headers)
	
	return result


def get_plus_info(body_json):
	token = body_json['access_token']
	headers = {'Authorization': 'Bearer ' + token}
	result = urlfetch.fetch(url=GPLUS_URL, method=urlfetch.GET, headers=headers)
	plus_json = json.loads(result.content)
	return plus_json
	
def handle_oauth(self, code, state):
	token_context = request_token(self, code)
	body_json = json.loads(token_context.content)
	plus_json = get_plus_info(body_json)
	
	logging.info(json.dumps(plus_json))
	template_values = {
		'firstName': plus_json['name']['givenName'], \
		'lastName': plus_json['name']['familyName'], \
		'googleUrl': plus_json['url'], \
		'stateVar': state
	}
	
	template = jinja_environment.get_template('oauth.html')
	# self.response.out.write(template.render(template_values))
	self.response.out.write(template.render(template_values))
	

def display_main(self):
	google_url = GOOGLE_SERVER + \
		"?client_id=" + CLIENT_ID + \
		"&redirect_uri=" + REDIRECT_URI + \
		"&response_type=code" + \
		"&scope=email" + \
		"&state=" + id_generator()
	template_values = {
		'google_url':google_url,
	}
	template = jinja_environment.get_template('index.html')
	self.response.out.write(template.render(template_values))
	
	
class MainPage(webapp2.RequestHandler):
    def get(self):
		
		code = self.request.get('code')
		state = self.request.get('state')
		if (code and state):
			#display_main(self)
			handle_oauth(self, code, state)
		
		else:
			display_main(self)

		
app = webapp2.WSGIApplication([
    ('/', MainPage),
], debug=True)