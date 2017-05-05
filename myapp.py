import os
import webapp2
import jinja2
import json
import logging
 
jinja_environment = jinja2.Environment(autoescape=True, loader=jinja2.FileSystemLoader(os.path.join(os.path.dirname(__file__), 'templates')))
googleServer = "https://accounts.google.com/o/oauth2/v2/auth"

#client ID: 1075487943853-i6t2ua56n8oo8960cmkhu7tona5u9bh9.apps.googleusercontent.com
#client secret: JcIf1764iYwahLxT9P5GBBYa

class MainPage(webapp2.RequestHandler):
    def get(self):
		template_values = {
			'hello':'world'
		}
		
		template = jinja_environment.get_template('index.html')
		self.response.out.write(template.render(template_values))


class OAuthHandler(webapp2.RequestHandler):
	def get(self):
		self.response.write(googleServer)
		
app = webapp2.WSGIApplication([
    ('/', MainPage),
	('/oauth', OAuthHandler),
], debug=True)