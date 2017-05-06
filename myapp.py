from google.appengine.api import urlfetch

import os
import webapp2
import jinja2
import json
import logging
import string
import random
import httplib
 
jinja_environment = jinja2.Environment(autoescape=True, loader=jinja2.FileSystemLoader(os.path.join(os.path.dirname(__file__), 'templates')))
GOOGLE_SERVER = "https://accounts.google.com/o/oauth2/v2/auth"

CLIENT_ID="1075487943853-i6t2ua56n8oo8960cmkhu7tona5u9bh9.apps.googleusercontent.com"
CLIENT_SECRET = "JcIf1764iYwahLxT9P5GBBYa"
REDIRECT_URI = "https://oauth2-166722.appspot.com/oauth"

TOKEN_URL = "https://www.googleapis.com/oauth2/v4/token"


# https://accounts.google.com/o/oauth2/v2/auth?
# client_id=1075487943853-i6t2ua56n8oo8960cmkhu7tona5u9bh9.apps.googleusercontent.com&
# redirect_uri=https://oauth2-166722.appspot.com/oauth&
# response_type=code&
# scope=email&
# state=SuperSecret9000

#output code: 4/O6WM1q_gA423I_fqIC1VSOJWRCHGuThKsivV8bDbTVg#

#token: ya29.GltBBOqKeBm6LY1EftxYGXpGYNHs8FhoI_1yZhDms7mGQ-rwMxBGaxKNjhTYwVCdo1xqNNh-NJf6AdOJO94RSBQz-lbbs5yQpfyWUO4ct1SFPRd8rS4M4kAAflfL

def id_generator(size=6, chars=string.ascii_uppercase + string.digits):
	return ''.join(random.choice(chars) for _ in range(size))


def request_token(self, code):
	headers = {
		'Content-Type': 'application/x-www-form-urlencoded'
	}
	payload = { \
		'code':code, \
		'client_id': CLIENT_ID, \
		'client_secret': CLIENT_SECRET, \
		'redirect_uri': REDIRECT_URI, \
		'grant_type': 'authorization_code'
	}
	result = urlfetch.fetch(\
		url=TOKEN_URL, \
		payload=payload, \
		method=urlfetch.POST, \
		headers=headers)
	return result
	
	
def handle_oauth(self, code):
	http = request_token(self, code)
	
	if (http.status_code > 200):
		template_values = {
			'message': 'An error occurred in your request',
			'info': 'No information returned'
		}
	
	else:
		template_values = {
			'message': 'Congratulations! You have been authorized.',
			'info': 'you are such a boss'
		}
		
	template = jinja_environment.get_template('oauth.html')
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
		if (code):
			handle_oauth(self, code)
		
		else:
			display_main(self)

		
app = webapp2.WSGIApplication([
    ('/', MainPage),
], debug=True)