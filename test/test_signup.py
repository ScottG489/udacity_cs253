import unittest
from unit4.signup import UserDataHandler, Signup, Encryption

from google.appengine.ext import testbed

class TestUserDataHandler(unittest.TestCase):
    # pylint: disable=R0904
    def setUp(self):    # pylint: disable=C0103
        self.data_handler = UserDataHandler()
        # First, create an instance of the Testbed class.
        self.testbed = testbed.Testbed()
        # Then activate the testbed, which prepares the service stubs for use.
        self.testbed.activate()
        # Next, declare which service stubs you want to use.
        self.testbed.init_datastore_v3_stub()
        self.testbed.init_memcache_stub()

    def tearDown(self):    # pylint: disable=C0103
        self.testbed.deactivate

    def test_page_entry_get_and_put(self):
        data = {}
        data['username'] = 'The username'
        data['password'] = 'The password'
        data['email'] = 'the@email.com'
        page_entry_id = self.data_handler.put(data['username'],
        data['password'], data['email'])

        actual = self.data_handler.get_by_id(page_entry_id)
        expected = data

        self.assertTrue(Encryption.is_valid_password(expected['username'],
            expected['password'], actual['password']))

    def test_get_all_page_entries(self):
        actual_input = {}
        actual_input['username'] = 'The username'
        actual_input['password'] = 'The password'
        actual_input['email'] = 'the@email.cm'

        self.data_handler.put(actual_input['username'],
        actual_input['password'], actual_input['email'])
        self.data_handler.put(actual_input['username'],
        actual_input['password'], actual_input['email'])

        actual = self.data_handler.get_all()

        # Might not be the best way to do this but everything needs to be equal
        # to validate...
        for item in actual:
            self.assertTrue(Encryption.is_valid_password(actual_input['username'],
                    actual_input['password'], item['password']))


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

class TestEncryption(unittest.TestCase):
    # pylint: disable=R0904
    def setUp(self):    # pylint: disable=C0103
        self.crypt = Encryption()

    def tearDown(self):    # pylint: disable=C0103
        pass

    def test_make_salt(self):
        salt1 = self.crypt.make_salt()
        salt2 = self.crypt.make_salt()

        self.assertNotEqual(salt1, salt2)

    def test_cookie_hash(self):
        user_id = 1
        user_id_hash = self.crypt.make_user_id_hash(user_id)
        self.assertTrue(self.crypt.is_valid_cookie(user_id, user_id_hash))

    def test_password_hash(self):
        username = 'username'
        password = 'password'
        hash_and_salt = self.crypt.make_password_hash(username, password)
        self.assertTrue(self.crypt.is_valid_password(username, password,
            hash_and_salt))


if __name__ == '__main__':
    #VERBOSITY = util.verbosity_helper()
    VERBOSITY = 1

    SUITE = unittest.TestLoader().loadTestsFromTestCase(TestUserSignup)
    unittest.TextTestRunner(verbosity=VERBOSITY).run(SUITE)
    SUITE = unittest.TestLoader().loadTestsFromTestCase(TestUserDataHandler)
    unittest.TextTestRunner(verbosity=VERBOSITY).run(SUITE)
    SUITE = unittest.TestLoader().loadTestsFromTestCase(TestEncryption)
    unittest.TextTestRunner(verbosity=VERBOSITY).run(SUITE)
