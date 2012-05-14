import unittest
from unit4.encryption import Encryption
from unit4.user import UserDataHandler

from google.appengine.ext import testbed

class TestUserDataHandler(unittest.TestCase):
    # pylint: disable=R0904
    def setUp(self):    # pylint: disable=C0103
        self.crypt = Encryption()
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

    def test_get_by_username(self):
        actual_input = {}
        actual_input['username'] = 'The username'
        actual_input['password'] = 'The password'
        actual_input['email'] = 'the@email.cm'

        self.data_handler.put(actual_input['username'],
        actual_input['password'], actual_input['email'])

        user_dict = self.data_handler.get_by_username(actual_input['username'])
        self.assertTrue(self.crypt.is_valid_password(actual_input['username'],
            actual_input['password'], user_dict['password']))
        self.assertEqual(actual_input['email'], user_dict['email'])


if __name__ == '__main__':
    #VERBOSITY = util.verbosity_helper()
    VERBOSITY = 1

    SUITE = unittest.TestLoader().loadTestsFromTestCase(TestUserDataHandler)
    unittest.TextTestRunner(verbosity=VERBOSITY).run(SUITE)
