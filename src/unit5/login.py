import cgi
import webapp2
import jinja2
import os
from encryption import Encryption
from user import UserDataHandler

#from google.appengine.ext import db

template_dir = os.path.join(os.path.dirname(__file__), 'views')
jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader(template_dir))

class PageHandler(webapp2.RequestHandler):
    def write_template(self, template_file, **params):
        template = jinja_env.get_template(template_file)
        self.response.out.write(template.render(params))

class LoginMainPage(PageHandler):
    def get(self):
        self.write_template('login.html')

    def post(self):
        self.response.headers['Content-Type'] = 'text/html'

        username = self.request.get('username')
        password = self.request.get('password')

        username = self.escape_html(username)

        user_list = UserDataHandler.get_by_username(username)
        if user_list and Encryption.is_valid_password(username, password,
                user_list[0].password):
            user = user_list[0]
            user_id = user.key().id()
            user_id_hash = Encryption.make_user_id_hash(user_id)
            self.response.headers.add_header('Set-Cookie',
                    'user_id=%(user_id)s|%(user_id_hash)s; Path=/'
                    % {'user_id': user_id, 'user_id_hash': user_id_hash})
            self.redirect('/unit5/welcome')
        else:
            self.write_template('login.html', username = username, login_error =
                    'invalid login')

    def escape_html(self, s):
        return cgi.escape(s, quote=True)
