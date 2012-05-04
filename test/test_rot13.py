import unittest
from unit2.rot13 import Rot13

class TestRot13(unittest.TestCase):
    # pylint: disable=R0904
    def setUp(self):    # pylint: disable=C0103
        self.rot13 = Rot13()

    def tearDown(self):    # pylint: disable=C0103
        pass

    def test_hello(self):
        expected = 'Uryyb'
        actual = self.rot13.rot13('Hello')
        self.assertEqual(actual, expected)

    def test_puncutation(self):
        expected = 'nfqs!'
        actual = self.rot13.rot13('asdf!')
        self.assertEqual(actual, expected)

    def test_whitespace(self):
        expected = 'n o p q '
        actual = self.rot13.rot13('a b c d ')
        self.assertEqual(actual, expected)

    def test_newline(self):
        expected = 'hi\nthere'
        actual = self.rot13.rot13('uv\ngurer')
        self.assertEqual(actual, expected)

    def test_html_escape(self): # Note: HTML escaping handled after the fact
        expected = 'fbzrgrkg</grkgnern>'
        actual = self.rot13.rot13('sometext</textarea>')
        self.assertEqual(actual, expected)


if __name__ == '__main__':
    #VERBOSITY = util.verbosity_helper()
    VERBOSITY = 1

    SUITE = unittest.TestLoader().loadTestsFromTestCase(TestRot13)
    unittest.TextTestRunner(verbosity=VERBOSITY).run(SUITE)
