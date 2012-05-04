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
from unit2.user_signup import UserSignup, UserSignupWelcome


class MainPage(webapp2.RequestHandler):
    def get(self):
        self.response.headers['Content-Type'] = 'text/html'
        self.response.out.write('<a href="unit2/rot13">unit2/rot13</a><br>')
        self.response.out.write('<a href="unit2/user_signup">unit2/user_signup</a>')


app = webapp2.WSGIApplication([('/', MainPage),
                            ('/unit1/hello_udacity', HelloUdacity),
                            ('/unit2/rot13', Rot13MainPage),
                            ('/unit2/user_signup', UserSignup),
                            ('/unit2/user_signup/welcome', UserSignupWelcome)],
                            debug=True)
