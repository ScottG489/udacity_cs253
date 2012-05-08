import webapp2
import jinja2
import os

template_dir = os.path.join(os.path.dirname(__file__), 'templates')
jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader(template_dir))

class PageHandler(webapp2.RequestHandler):
    pass

class FrontPageMainPage(PageHandler):
    pass

class EntryFormMainPage(PageHandler):
    def get(self):
        template = jinja_env.get_template('entry_form.html')
        self.response.out.write(template.render())

    def post(self):
        subject = self.request.get('subject')
        content = self.request.get('content')
        if self.is_valid_input(subject) and self.is_valid_input(content):
            self.response.out.write('success')
        else:
            self.response.out.write('fail')

    def is_valid_input(self, content):
        if content != '':
            return True

        return False

class PageEntryMainPage(PageHandler):
    def get(self):
        pass
