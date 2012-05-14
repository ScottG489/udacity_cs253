import re
import cgi
import webapp2
import jinja2
import os
import random
import string
import hashlib

from google.appengine.ext import db

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
            self.redirect('/unit4/signup/welcome')

    def escape_html(self, s):
        return cgi.escape(s, quote=True)

class Encryption(object):
    @staticmethod
    def make_salt():
        return ''.join(random.sample(string.letters,  5))

    @staticmethod
    def make_user_id_hash(user_id, salt = None):
        user_id = str(user_id)
        if not salt:
            salt = Encryption.make_salt()
        value_hash = hashlib.sha256(user_id + salt).hexdigest()
        return '%s|%s' % (value_hash, salt)

    @staticmethod
    def is_valid_cookie(user_id, user_id_hash):
        salt = user_id_hash.split('|')[1]
        return user_id_hash == Encryption.make_user_id_hash(user_id, salt)

    @staticmethod
    def make_password_hash(name, pw, salt = None):
        if not salt:
            salt = Encryption.make_salt()
        value_hash = hashlib.sha256(name + pw + salt).hexdigest()
        return '%s,%s' % (value_hash, salt)

    @staticmethod
    def is_valid_password(username, password, password_hash):
        salt = password_hash.split(',')[1]
        return password_hash == Encryption.make_password_hash(username, password, salt)

class User(db.Model):
    username = db.StringProperty(required = True)
    password = db.StringProperty(required = True)
    email = db.StringProperty()

class UserDataHandler(object):
    @staticmethod
    def get_by_id(user_id):
        "Returns a dict given a user id"
        # TODO: Why can't to_dict() be called on PageEntry.get_by_id()?
        user = User.get_by_id(user_id)
        return {'username': user.username, 'password': user.password, 'email':
                user.email}

    @staticmethod
    def put(username, password, email = ''):
        password_hash = Encryption.make_password_hash(username, password)
        return User(username = username, password = password_hash, email = email).put().id()

    @staticmethod
    def get_all():
        "Returns all page entries as dict's in a list"
        users = db.GqlQuery('SELECT * FROM User')
        return [{'username': user.username, 'password': user.password, 'email': user.email}
                for user in users]

class Signup(object):
    def is_valid_username(self, username):
        if username != '' and re.search('^[a-zA-Z0-9_-]{3,20}$', username):    # Successful match
            return True

        return False

    def is_unique_username(self, username):
        all_users = UserDataHandler.get_all()
        for user in all_users:
            if username == user['username']:
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

class SignupWelcome(PageHandler):
    def get(self):
        self.response.headers['Content-Type'] = 'text/html'
        user_id_cookie = self.request.cookies.get('user_id')
        user_id = user_id_cookie.split('|')[0]
        user_id_hash = '|'.join(user_id_cookie.split('|')[1:])

        if Encryption.is_valid_cookie(user_id, user_id_hash):
            user = UserDataHandler.get_by_id(int(user_id))
            self.response.out.write('Welcome, <b>' + user.get('username') + '</b>!')
        else:
            self.redirect('/unit4/signup')
