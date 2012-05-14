import webapp2
import jinja2
import os
from encryption import Encryption
from user import UserDataHandler

template_dir = os.path.join(os.path.dirname(__file__), 'views')
jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader(template_dir))

class PageHandler(webapp2.RequestHandler):
    def write_template(self, template_file, **params):
        template = jinja_env.get_template(template_file)
        self.response.out.write(template.render(params))

class WelcomeMainPage(PageHandler):
    def get(self):
        self.response.headers['Content-Type'] = 'text/html'
        user_id_cookie = self.request.cookies.get('user_id')
        user_id = user_id_cookie.split('|')[0]
        user_id_hash = user_id_cookie.split('|')[1]

        if Encryption.is_valid_cookie(user_id, user_id_hash):
            user = UserDataHandler.get_by_id(int(user_id))
            self.response.out.write('Welcome, <b>' + user.get('username') + '</b>!')
        else:
            self.redirect('/unit4/signup')
