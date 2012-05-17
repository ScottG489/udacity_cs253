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

# TODO: Split this up into appropriate class files and projects.
# TODO: Add logging.
# TODO: Implement testing.

import webapp2
from unit1.hello_udacity import HelloUdacity
from unit2.rot13 import Rot13MainPage
from unit2.user_signup import UserSignupMainPage, UserSignupWelcome
import unit3.blog
import unit4.signup
import unit4.login
import unit4.welcome
import unit4.logout
import unit5.blog
import unit5.signup
import unit5.login
import unit5.welcome
import unit5.logout
import unit5.json_blog



class MainPage(webapp2.RequestHandler):
    def get(self):
        self.response.headers['Content-Type'] = 'text/html'
        self.response.out.write('<a href="unit2/rot13">unit2/rot13</a><br>')
        self.response.out.write('<a href="unit2/user_signup">unit2/user_signup</a><br>')
        self.response.out.write('<a href="unit3/blog">unit3/blog</a><br>')
        self.response.out.write('<a href="unit4/signup">unit4/signup</a><br>')
        self.response.out.write('<a href="unit4/login">unit4/login</a><br>')
        self.response.out.write('<a href="unit4/logout">unit4/logout</a><br>')
        self.response.out.write('<a href="unit5">unit5</a><br>')


app = webapp2.WSGIApplication([('/', MainPage),
                            ('/unit1/hello_udacity', HelloUdacity),
                            ('/unit2/rot13', Rot13MainPage),
                            ('/unit2/user_signup', UserSignupMainPage),
                            ('/unit2/user_signup/welcome', UserSignupWelcome),
                            ('/unit3/blog', unit3.blog.FrontPageMainPage),
                            ('/unit3/blog/newpost', unit3.blog.EntryFormMainPage),
                            ('/unit3/blog/([0-9]+)', unit3.blog.PageEntryMainPage),
                            ('/unit4/signup', unit4.signup.SignupMainPage),
                            ('/unit4/welcome', unit4.welcome.WelcomeMainPage),
                            ('/unit4/login', unit4.login.LoginMainPage),
                            ('/unit4/logout', unit4.logout.LogoutMainPage),
                            ('/unit5', unit5.blog.FrontPageMainPage),
                            ('/unit5/.json', unit5.json_blog.FrontPageJSON),
                            ('/unit5/newpost', unit5.blog.EntryFormMainPage),
                            ('/unit5/([0-9]+)', unit5.blog.PageEntryMainPage),
                            ('/unit5/([0-9]+).json', unit5.json_blog.PageEntryJSON),
                            ('/unit5/signup', unit5.signup.SignupMainPage),
                            ('/unit5/welcome', unit5.welcome.WelcomeMainPage),
                            ('/unit5/login', unit5.login.LoginMainPage),
                            ('/unit5/logout', unit5.logout.LogoutMainPage)],
                            debug=True)
