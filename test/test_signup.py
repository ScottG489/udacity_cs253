import unittest
from unit4.signup import UserDataHandler, Signup

from google.appengine.ext import testbed

# TODO: Helper functions to reduce code duplication.
class TestUserSignup(unittest.TestCase):
    # pylint: disable=R0904
    def setUp(self):    # pylint: disable=C0103
        self.signup = Signup()

        self.data_handler = UserDataHandler()
        # First, create an instance of the Testbed class.
        self.testbed = testbed.Testbed()
        # Then activate the testbed, which prepares the service stubs for use.
        self.testbed.activate()
        # Next, declare which service stubs you want to use.
        self.testbed.init_datastore_v3_stub()
        self.testbed.init_memcache_stub()

    def tearDown(self):    # pylint: disable=C0103
        pass

    def test_valid_username(self):
        actual = self.signup.is_valid_username('asdf')
        self.assertTrue(actual) 

    def test_username_exists(self):
        actual_input = {}
        actual_input['username'] = 'The username'
        actual_input['password'] = 'The password'
        actual_input['email'] = 'the@email.cm'

        self.data_handler.put(actual_input['username'],
        actual_input['password'], actual_input['email'])

        self.assertFalse(self.signup.is_unique_username(actual_input['username']))

    def test_username_length(self): # 2 < username length < 21
        actual = self.signup.is_valid_username('')
        self.assertFalse(actual)
        actual = self.signup.is_valid_username('a')
        self.assertFalse(actual)
        actual = self.signup.is_valid_username('ab')
        self.assertFalse(actual)
        actual = self.signup.is_valid_username('abcdefghijklmnopqrstu')
        self.assertFalse(actual)
        actual = self.signup.is_valid_username('abcdefghijklmnopqrst')
        self.assertTrue(actual)

    def test_username_special_characters(self):
        actual = self.signup.is_valid_username('asdf!')
        self.assertFalse(actual)
        actual = self.signup.is_valid_username('as<df')
        self.assertFalse(actual)
        actual = self.signup.is_valid_username('adfd`')
        self.assertFalse(actual)

    def test_valid_password(self):
        actual = self.signup.is_valid_password('pass')
        self.assertTrue(actual)

    def test_password_length(self): # 2 < password length < 21
        actual = self.signup.is_valid_password('')
        self.assertFalse(actual)
        actual = self.signup.is_valid_password('a')
        self.assertFalse(actual)
        actual = self.signup.is_valid_password('ab')
        self.assertFalse(actual)
        actual = self.signup.is_valid_password('abcdefghijklmnopqrstu')
        self.assertFalse(actual)
        actual = self.signup.is_valid_password('abcdefghijklmnopqrst')
        self.assertTrue(actual)

    def test_password_special_characters(self):
        actual = self.signup.is_valid_password('asdf!')
        self.assertTrue(actual)
        actual = self.signup.is_valid_password('as<df')
        self.assertTrue(actual)
        actual = self.signup.is_valid_password('adfd`')
        self.assertTrue(actual)

    def test_valid_email(self):
        actual = self.signup.is_valid_email('asdf@sadfas.com')
        self.assertTrue(actual)
        actual = self.signup.is_valid_email('')
        self.assertTrue(actual)

    def test_email_whitespace(self): # 2 < username length < 21
        actual = self.signup.is_valid_email('as df@safd.com')
        self.assertFalse(actual)

if __name__ == '__main__':
    #VERBOSITY = util.verbosity_helper()
    VERBOSITY = 1

    SUITE = unittest.TestLoader().loadTestsFromTestCase(TestUserSignup)
    unittest.TextTestRunner(verbosity=VERBOSITY).run(SUITE)
