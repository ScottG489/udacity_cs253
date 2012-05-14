import unittest
from unit4.encryption import Encryption

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

    SUITE = unittest.TestLoader().loadTestsFromTestCase(TestEncryption)
    unittest.TextTestRunner(verbosity=VERBOSITY).run(SUITE)
