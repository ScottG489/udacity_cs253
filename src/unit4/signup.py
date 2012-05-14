import re
import cgi
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

class SignupMainPage(PageHandler):
    def get(self):
        self.write_template('signup.html')

    def post(self):
        signup = Signup()
        self.response.headers['Content-Type'] = 'text/html'

        errors = {}
        username = self.request.get('username')
        password = self.request.get('password')
        verify = self.request.get('verify')
        email = self.request.get('email')

        if not signup.is_valid_username(username):
            errors['username_error'] = 'Invalid username.'
        elif not signup.is_unique_username(username):
            errors['username_error'] = 'Username taken.'
        if not signup.is_valid_password(password):
            errors['password_error'] = 'Invalid password.'
        elif password != verify:
            errors['verify_error'] = 'Passwords don\'t match.'
        if not signup.is_valid_email(email):
            errors['email_error'] = 'Invalid email.'

        username = self.escape_html(username)
        email = self.escape_html(email)

        if errors:
            self.write_template('signup.html', username = username, email =
                    email, **errors)
        else:
            user_id = UserDataHandler.put(username, password, email)
            user_id_hash = Encryption.make_user_id_hash(user_id)
            self.response.headers.add_header('Set-Cookie',
                    'user_id=%(user_id)s|%(user_id_hash)s; Path=/'
                    % {'user_id': user_id, 'user_id_hash': user_id_hash})
            self.redirect('/unit4/welcome')

    def escape_html(self, s):
        return cgi.escape(s, quote=True)

class Signup(object):
    def is_valid_username(self, username):
        if username != '' and re.search('^[a-zA-Z0-9_-]{3,20}$', username):    # Successful match
            return True

        return False

    def is_unique_username(self, username):
        all_users = UserDataHandler.get_all()
        for user in all_users:
            if username == user.username:
                return False

        return True

    def is_valid_password(self, password):
        if password != '' and re.search('^.{3,20}$', password):    # Successful match
            return True

        return False

    def is_valid_email(self, email):
        if email == '' or re.search('^[\S]+@[\S]+\.[\S]+$', email):    # Successful match
            return True

        return False
