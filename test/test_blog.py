import unittest
#from unit3.blog import FrontPageMainPage
from unit3.blog import EntryFormMainPage
#from unit3.blog import PageEntryMainPage

class TestEntryForm(unittest.TestCase):
    # pylint: disable=R0904
    def setUp(self):    # pylint: disable=C0103
        self.entry_form = EntryFormMainPage()
        pass

    def tearDown(self):    # pylint: disable=C0103
        pass

    def test_entry_form_input(self):
        content = ''
        self.assertFalse(self.entry_form.is_valid_input(content))
        content = 'this is some content'
        self.assertTrue(self.entry_form.is_valid_input(content))

        subject = ''
        self.assertFalse(self.entry_form.is_valid_input(subject))
        subject = 'this is some subject'
        self.assertTrue(self.entry_form.is_valid_input(subject))


if __name__ == '__main__':
    #VERBOSITY = util.verbosity_helper()
    VERBOSITY = 1

    SUITE = unittest.TestLoader().loadTestsFromTestCase(TestEntryForm)
    unittest.TextTestRunner(verbosity=VERBOSITY).run(SUITE)
