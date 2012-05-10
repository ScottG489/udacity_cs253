import unittest
#from unit3.blog import FrontPageMainPage
from unit3.blog import EntryFormMainPage, PageEntryDataHandler
#from unit3.blog import PageEntryMainPage
from google.appengine.api import memcache
from google.appengine.ext import db
from google.appengine.ext import testbed

class TestEntryForm(unittest.TestCase):
    # pylint: disable=R0904
    def setUp(self):    # pylint: disable=C0103
        self.entry_form = EntryFormMainPage()
        pass

    def tearDown(self):    # pylint: disable=C0103
        pass

    def test_entry_form_input(self):
        subject = ''
        self.assertFalse(self.entry_form.is_valid_input(subject))
        subject = 'this is some subject'
        self.assertTrue(self.entry_form.is_valid_input(subject))

        content = ''
        self.assertFalse(self.entry_form.is_valid_input(content))
        content = 'this is some content'
        self.assertTrue(self.entry_form.is_valid_input(content))

class TestPageEntryDataHandler(unittest.TestCase):
    # pylint: disable=R0904
    def setUp(self):    # pylint: disable=C0103
        self.data_handler = PageEntryDataHandler()
        # First, create an instance of the Testbed class.
        self.testbed = testbed.Testbed()
        # Then activate the testbed, which prepares the service stubs for use.
        self.testbed.activate()
        # Next, declare which service stubs you want to use.
        self.testbed.init_datastore_v3_stub()
        self.testbed.init_memcache_stub()

    def tearDown(self):    # pylint: disable=C0103
        self.testbed.deactivate

    def test_page_entry_get_and_get(self):
        actual = {}
        actual['subject'] = 'The subject'
        actual['content'] = 'The content'
        page_entry_id = self.data_handler.put(actual['subject'],
        actual['content'])

        expected = self.data_handler.get_by_id(page_entry_id)

        self.assertEqual(actual, expected)

    def test_get_all_page_entries(self):
        actual_input = {}
        actual_input['subject'] = 'The subject'
        actual_input['content'] = 'The content'
        self.data_handler.put(actual_input['subject'],
        actual_input['content'])
        self.data_handler.put(actual_input['subject'],
        actual_input['content'])
        actual = self.data_handler.get_all()

        expected = [actual_input, actual_input]

        self.assertEqual(actual, expected)


if __name__ == '__main__':
    #VERBOSITY = util.verbosity_helper()
    VERBOSITY = 1

    SUITE = unittest.TestLoader().loadTestsFromTestCase(TestEntryForm)
    unittest.TextTestRunner(verbosity=VERBOSITY).run(SUITE)
    SUITE = unittest.TestLoader().loadTestsFromTestCase(TestPageEntryDataHandler)
    unittest.TextTestRunner(verbosity=VERBOSITY).run(SUITE)
