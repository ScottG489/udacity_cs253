import unittest
from unit2.rot13 import Rot13

class TestRot13(unittest.TestCase):
    # pylint: disable=R0904
    def setUp(self):    # pylint: disable=C0103
        self.rot13 = Rot13()

    def tearDown(self):    # pylint: disable=C0103
        pass

    def foo(self):
        self.rot13.rot13('hello')


if __name__ == '__main__':
    #VERBOSITY = util.verbosity_helper()
    VERBOSITY = 1

    SUITE = unittest.TestLoader().loadTestsFromTestCase(TestRot13)
    unittest.TextTestRunner(verbosity=VERBOSITY).run(SUITE)
