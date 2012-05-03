import cgi
import webapp2

class MainPage(webapp2.RequestHandler):
    def get(self):
        self.response.headers['Content-Type'] = 'text/html'
        self.write_form()

    def post(self):
        rot13 = Rot13()
        self.response.headers['Content-Type'] = 'text/html'
        text = self.request.get('text')
        new_text = rot13.rot13(text)
        new_text = self.escape_html(new_text)
        self.write_form(new_text)

    def escape_html(self, s):
        return cgi.escape(s, quote=True)

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

class Rot13(object):
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
