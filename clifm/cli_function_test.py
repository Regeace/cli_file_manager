import unittest
from cli_functions import *
from _utils import make_test_dir_and_files, delete_test_dir_and_files


class FunctionsTest(unittest.TestCase):
    def setUp(self):
        make_test_dir_and_files()

    def test_copy_file(self):
        copy_file('test_file1.txt')
        copy_file('test_file1.txt')

        self.assertTrue(os.path.exists('test_file1.txt'))
        self.assertTrue(os.path.exists('copy_test_file1.txt'))
        self.assertTrue(os.path.exists('another_copy_test_file1.txt'))

    def tearDown(self):
        delete_test_dir_and_files()


if __name__ == '__main__':
    unittest.main(argv=['', ], exit=False)
