import os
import unittest


class TestInitializeDB(unittest.TestCase):

    def test_usage(self):
        from ..scripts.initializedb import main
        with self.assertRaises(SystemExit):
            main(argv=['foo'])

    def test_run(self):
        from ..scripts.initializedb import main
        main(argv=['foo', 'development_test.ini'])
        self.assertTrue(os.path.exists('jobtrack2_test.sqlite'))
        os.remove('jobtrack2_test.sqlite')