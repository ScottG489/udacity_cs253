import webapp2
import logging
import jinja2
import cgi
import os
import blog
import json

from google.appengine.ext import db

template_dir = os.path.join(os.path.dirname(__file__), 'views')
jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader(template_dir))

class FrontPageJSON(blog.PageHandler):
    def get(self):
        page_entry = blog.PageEntryDataHandler.get_all()
        self.response.headers['Content-Type'] = 'application/json'
        self.response.out.write(json.dumps(page_entry))

class PageEntryJSON(blog.PageHandler):
    def get(self, page_entry_id):
        page_entry = blog.PageEntryDataHandler.get_by_id(int(page_entry_id))
        self.response.headers['Content-Type'] = 'application/json'
        self.response.out.write(json.dumps(page_entry))
