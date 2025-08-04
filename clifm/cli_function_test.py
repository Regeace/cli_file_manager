import os
import unittest
from cli_functions import *
from _utils import make_test_dir_and_files, delete_test_dir_and_files


class FunctionsTest(unittest.TestCase):
    test_dir = 'files_for_tests'
    test_dir_inner = 'files_for_tests\\files_for_tests_inner'
    test_dir_inner_name = 'files_for_tests_inner'
    test_file1 = 'test_file1.txt'
    test_file2 = 'test_file2.txt'
    test_file3 = 'test_file3.txt'

    def setUp(self):
        make_test_dir_and_files()

    def test_count_files(self):
        self.assertEqual(count_files(self.test_dir), 6)

    def test_find_files(self):
        answer1 = [
            (self.test_dir, self.test_file1),
            (self.test_dir_inner, self.test_file1)
        ]
        answer2 = [
            (self.test_dir, self.test_file1),
            (self.test_dir, self.test_file2),
            (self.test_dir, self.test_file3),
            (self.test_dir_inner, self.test_file1),
            (self.test_dir_inner, self.test_file2),
            (self.test_dir_inner, self.test_file3)
        ]

        self.assertEqual(find_files(self.test_dir, self.test_file1), answer1)
        self.assertEqual(find_files(self.test_dir, '1.txt$'), answer1)
        self.assertEqual(find_files(self.test_dir, '1'), answer1)

        self.assertEqual(find_files(self.test_dir, '[0-9]'), answer2)
        self.assertEqual(find_files(self.test_dir, 'test'), answer2)
        self.assertEqual(find_files(self.test_dir, r'\d'), answer2)

    def test_copy_file(self):
        os.chdir(self.test_dir)
        copy_file(self.test_file1)
        copy_file(self.test_file1)

        self.assertTrue(os.path.exists(self.test_file1))
        self.assertTrue(os.path.exists(f'copy_{self.test_file1}'))
        self.assertTrue(os.path.exists(f'another_copy_{self.test_file1}'))

        os.chdir('..')

    def test_add_date_to_name(self):
        """Проверяется наличие файла с новым именем и отсутствие файла со старым именем в каталоге и подкаталоге,
        далее проверяется применимость функции к отдельному файлу"""
        add_date_to_name(self.test_dir, recursive=True)
        os.chdir(self.test_dir)

        self.assertTrue(os.path.exists(f'{self.test_file1[:-4]}_{str(date.today())}{self.test_file1[-4:]}'))
        self.assertFalse(os.path.exists(self.test_file1))
        os.chdir(self.test_dir_inner_name)
        self.assertTrue(os.path.exists(f'{self.test_file3[:-4]}_{str(date.today())}{self.test_file3[-4:]}'))
        self.assertFalse(os.path.exists(self.test_file3))
        os.chdir('..')

        make_file('test_file.txt')
        add_date_to_name('test_file.txt')

        self.assertTrue(os.path.exists(f'test_file_{str(date.today())}.txt'))
        self.assertFalse(os.path.exists('test_file.txt'))

        os.chdir('..')

    def tearDown(self):
        delete_test_dir_and_files()


if __name__ == '__main__':
    unittest.main(argv=['', ], exit=False)
