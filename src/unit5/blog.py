import webapp2
import logging
import jinja2
import cgi
import os

from google.appengine.ext import db

template_dir = os.path.join(os.path.dirname(__file__), 'views')
jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader(template_dir))

class PageHandler(webapp2.RequestHandler):
    def write_template(self, template_file, **params):
        template = jinja_env.get_template(template_file)
        self.response.out.write(template.render(params))

class FrontPageMainPage(PageHandler):
    def get(self):
        page_entry = PageEntryDataHandler.get_all()
        self.write_template('front_page.html', page_entries = page_entry)

class EntryFormMainPage(PageHandler):
    def get(self):
        self.write_template('entry_form.html')

    def post(self):
        subject = self.request.get('subject')
        content = self.request.get('content')
        subject = self.escape_html(subject)
        content = self.escape_html(content)
        if self.is_valid_input(subject) and self.is_valid_input(content):
            page_entry_id = PageEntryDataHandler.put(subject, content)
            self.redirect('/unit5/%s' % str(page_entry_id))
        else:
            self.write_template('entry_form.html', subject = subject, content = content, error = 'error')

    def escape_html(self, s):
        return cgi.escape(s, quote=True)

    def is_valid_input(self, content):
        if content != '':
            return True

        return False

class PageEntryDataHandler(object):
    @staticmethod
    def get_by_id(page_entry_id):
        "Returns a dict given a page entry id"
    # TODO: Why can't to_dict() be called on PageEntry.get_by_id()?
        page_entry = PageEntry.get_by_id(page_entry_id)
        return {'subject': page_entry.subject, 'content': page_entry.content}

    @staticmethod
    def put(subject, content):
        return PageEntry(subject = subject, content = content).put().id()

    @staticmethod
    def get_all():
        "Returns all page entries as dict's in a list"
        page_entries = db.GqlQuery('SELECT * FROM PageEntry ORDER BY created\
                DESC')
        #p = page_entries.fetch(100)
        #db.delete(p)
        #return
        return [{'subject': page_entry.subject, 'content': page_entry.content}
                for page_entry in page_entries]

class PageEntry(db.Model):
    subject = db.StringProperty(required = True)
    content = db.TextProperty(required = True)
    created = db.DateTimeProperty(auto_now_add = True)

class PageEntryMainPage(PageHandler):
    def get(self, page_entry_id):
        page_entry = PageEntryDataHandler.get_by_id(int(page_entry_id))
        self.write_template('page_entry.html', **page_entry)
