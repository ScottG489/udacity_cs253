import re
import cgi
import webapp2

class UserSignupMainPage(webapp2.RequestHandler):
    def get(self):
        self.write_form()

    def post(self):
        rot13 = UserSignup()
        self.response.headers['Content-Type'] = 'text/html'

        errors = {}
        username = self.request.get('username')
        password = self.request.get('password')
        verify = self.request.get('verify')
        email = self.request.get('email')

        if not rot13.is_valid_username(username):
            errors['username_error'] = 'Invalid username.'
        if not rot13.is_valid_password(password):
            errors['password_error'] = 'Invalid password.'
        elif password != verify:
            errors['verify_error'] = 'Passwords don\'t match.'
        if not rot13.is_valid_email(email):
            errors['email_error'] = 'Invalid email.'

        username = self.escape_html(username)
        email = self.escape_html(email)

        if errors:
            self.write_form(username, email, **errors)
        else:
            self.redirect('/unit2/user_signup/welcome?username=' + username)

    def escape_html(self, s):
        return cgi.escape(s, quote=True)

    def write_form(self, username='', email='', username_error='',
            password_error='', verify_error='', email_error=''):
        self.form="""
        <h1>User Signup</h1>
        <form method="post">
            <label>Username
                <input name="username" type="text" value="%(username)s">
            </label>%(username_error)s
            <br>
            <label>Password
                <input name="password" type="password">
            </label>%(password_error)s
            <br>
            <label>Verify Password
                <input name="verify" type="password">
            </label>%(verify_error)s
            <br>
            <label>Email (optional)
                <input name="email" type="text" value="%(email)s">
            </label>%(email_error)s
            <br>
            <input type="submit" />
        </form>
        """
        self.response.out.write(self.form% {"username": username, "email":
            email, 'username_error': username_error, 'password_error':
            password_error, 'verify_error': verify_error, 'email_error': email_error})

class UserSignup(object):
    def is_valid_username(self, username):
        if username != '' and re.search('^[a-zA-Z0-9_-]{3,20}$', username):    # Successful match
            return True

        return False

    def is_valid_password(self, password):
        if password != '' and re.search('^.{3,20}$', password):    # Successful match
            return True

        return False

    def is_valid_email(self, email):
        if email == '' or re.search('^[\S]+@[\S]+\.[\S]+$', email):    # Successful match
            return True

        return False

class UserSignupWelcome(webapp2.RequestHandler):
    def get(self):
        self.response.headers['Content-Type'] = 'text/html'
        self.response.out.write('Welcome, <b>' + self.request.get('username') + '</b>!')
