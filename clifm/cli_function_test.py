import unittest
from cli_functions import *
from _utils import make_test_dir_and_files, delete_test_dir_and_files


class FunctionsTest(unittest.TestCase):
    def setUp(self):
        make_test_dir_and_files()

    def test_count_files(self):
        self.assertEqual(count_files('files_for_tests'), 6)

    def test_find_files(self):
        answer1 = [
        ('files_for_tests', 'test_file1.txt'),
        ('files_for_tests\\files_for_tests_inner', 'test_file1.txt')
        ]
        answer2 = [
        ('files_for_tests', 'test_file1.txt'),
        ('files_for_tests', 'test_file2.txt'),
        ('files_for_tests', 'test_file3.txt'),
        ('files_for_tests\\files_for_tests_inner', 'test_file1.txt'),
        ('files_for_tests\\files_for_tests_inner', 'test_file2.txt'),
        ('files_for_tests\\files_for_tests_inner', 'test_file3.txt')
        ]

        self.assertEqual(find_files('files_for_tests', 'test_file1.txt'), answer1)
        self.assertEqual(find_files('files_for_tests', '1.txt$'), answer1)
        self.assertEqual(find_files('files_for_tests', '1'), answer1)

        self.assertEqual(find_files('files_for_tests', '[0-9]'), answer2)
        self.assertEqual(find_files('files_for_tests', 'test'), answer2)
        self.assertEqual(find_files('files_for_tests', r'\d'), answer2)

    def test_copy_file(self):
        os.chdir('files_for_tests')
        copy_file('test_file1.txt')
        copy_file('test_file1.txt')

        self.assertTrue(os.path.exists('test_file1.txt'))
        self.assertTrue(os.path.exists('copy_test_file1.txt'))
        self.assertTrue(os.path.exists('another_copy_test_file1.txt'))

        os.chdir('..')

    def tearDown(self):
        delete_test_dir_and_files()


if __name__ == '__main__':
    unittest.main(argv=['', ], exit=False)
