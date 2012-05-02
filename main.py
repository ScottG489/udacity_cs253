#!/usr/bin/env python2
#
# Copyright 2007 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
import webapp2
import cgi
import re


class MainPage(webapp2.RequestHandler):
    def get(self):
        self.response.headers['Content-Type'] = 'text/html'
        self.response.out.write('<a href="unit2/rot13">unit2/rot13</a><br>')
        self.response.out.write('<a href="unit2/user_signup">unit2/user_signup</a>')

class UserSignup(webapp2.RequestHandler):
#    def __init__(self):

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


    def get(self):
        self.write_form()

    def post(self):
        errors = {}
        username = self.request.get('username')
        password = self.request.get('password')
        verify = self.request.get('verify')
        email = self.request.get('email')
        # XXX: ESCAPE INPUT FOR HTML
        if not self.validate_username(username):
            errors['username_error'] = 'Invalid username.'
        if not self.validate_password(password):
            errors['password_error'] = 'Invalid password.'
        if not self.validate_password_verify(password, verify):
            errors['verify_error'] = 'Passwords don\'t match.'
        if not self.validate_email(email):
            errors['email_error'] = 'Invalid email.'

        username = self.escape_html(username)
        email = self.escape_html(email)

        if errors:
            self.write_form(username, email, **errors)

    def escape_html(self, s):
        return cgi.escape(s, quote=True)

    def validate_username(self, username):
        if username != '' and re.search('^[a-zA-Z0-9_-]{3,20}$', username):    # Successful match
            return username

        return None

    def validate_password(self, password):
        if password != '' and re.search('^.{3,20}$', password):    # Successful match
            return password

        return None

    def validate_password_verify(self, password, verify):
        if password == verify:
            return verify

        return None

    def validate_email(self, email):
        if email == '' or re.search('^[\S]+@[\S]+\.[\S]+$', email):    # Successful match
            return email

        return None

class Rot13(webapp2.RequestHandler):
    def get(self):
        #self.response.headers['Content-Type'] = 'text/plain'
        self.write_form()

    def post(self):
        self.response.headers['Content-Type'] = 'text/html'
        text = self.request.get('text')
        new_text = self.rot13(text) 
        new_text = self.escape_html(new_text)
        self.write_form(new_text)

    def write_form(self, text=''):
        form="""
        <h1>ROT13</h1>
        <form method="post">
            <textarea name="text" style="height: 100px; width: 400px;">%(text)s</textarea>
            <br>
            <input type="submit" />
        </form>
        """

        self.response.out.write(form % {"text": text})

    def escape_html(self, s):
        return cgi.escape(s, quote=True)

    def rot13(self, s):
        rot13_s = ""

        lower = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l',
                'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x',
                'y', 'z']
        upper = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L',
                'M', 'N','O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X',
                'Y', 'Z']
        lower_len = len(lower)
        upper_len = len(upper)

        for char in s:
            if char in lower:
                rot13_s += lower[(lower.index(char) + 13) % lower_len]
            elif char in upper:
                rot13_s += upper[(upper.index(char) + 13) % upper_len]
            else:
                rot13_s += char
        return rot13_s


#class TestHandler(webapp2.RequestHandler):
#    def post(self):
#        text = self.request.get("text")
#        self.response.out.write(text)
#
#        self.response.headers['Content-Type'] = 'text/plain'
#        self.response.out.write(self.request)

app = webapp2.WSGIApplication([('/', MainPage),
                            ('/unit2/rot13', Rot13),
                            ('/unit2/user_signup', UserSignup)],
                            debug=True)
