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

        self.assertEqual(find_files(self.test_dir, self.test_file1, show_result=False), answer1)
        self.assertEqual(find_files(self.test_dir, '1.txt$', show_result=False), answer1)
        self.assertEqual(find_files(self.test_dir, '1', show_result=False), answer1)

        self.assertEqual(find_files(self.test_dir, '[0-9]', show_result=False), answer2)
        self.assertEqual(find_files(self.test_dir, 'test', show_result=False), answer2)
        self.assertEqual(find_files(self.test_dir, r'\d', show_result=False), answer2)

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

    def test_show_size(self):
        """Для проверки в 3 файла из разных каталогов добавляется строка размером 52 байта"""
        os.chdir(self.test_dir)
        with open(self.test_file1, 'w', encoding='utf-8') as f1:
            f1.write('Тестовый текст тестирования')
        os.chdir(self.test_dir_inner_name)
        with open(self.test_file2, 'w', encoding='utf-8') as f2:
            f2.write('Тестовый текст тестирования')
        with open(self.test_file3, 'w', encoding='utf-8') as f3:
            f3.write('Тестовый текст тестирования')
        os.chdir('..')
        os.chdir('..')
        dict_of_sizes_to_test = show_size(self.test_dir)

        self.assertEqual(dict_of_sizes_to_test[self.test_dir], 156)
        self.assertEqual(dict_of_sizes_to_test[self.test_dir_inner_name], 104)
        self.assertEqual(dict_of_sizes_to_test[self.test_file1], 52)
        self.assertEqual(dict_of_sizes_to_test[self.test_file3], 0)

    def tearDown(self):
        delete_test_dir_and_files()


if __name__ == '__main__':
    unittest.main(argv=['', ], exit=False)
