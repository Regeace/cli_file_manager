import unittest
from os import chdir
from sys import executable
from subprocess import run
from _utils import make_test_dir_and_files, delete_test_dir_and_files

'''При некорректной работе тестов во время вывода кириллицы из stdout заменить в locale кодировку на cp65001'''


class TestCli(unittest.TestCase):
    def setUp(self):
        make_test_dir_and_files()

    def test_cli_valid_expressions(self):
        test_cases = [
            ('count', r'clifm\files_for_tests', '6'),
            ('date', r'clifm\files_for_tests', 'К именам файлов в каталоге добавлена дата их создания'),
            ('copy', r'clifm\files_for_tests\files_for_tests_inner\test_file1.txt', 'Создана копия файла')
        ]

        for magic_word, name_path, answer in test_cases:
            chdir('..')
            with self.subTest(magic_word=magic_word, name_path=name_path, answer=answer):
                cli_result = run([executable, 'cli_file_manager.py', magic_word, name_path], capture_output=True,
                                 text=True)
                print(f'Должно быть: {answer},\nполучено в тесте: {cli_result.stdout[:-1]}\n')
                self.assertEqual(answer, cli_result.stdout[:-1])
            chdir('clifm')

    def test_cli_valid_expressions_long(self):
        """"Проверяет работу программы CLI при использовании 4 слов в написании команды"""
        chdir('..')
        cli_result = run([executable, 'cli_file_manager.py', 'find',
                          r'clifm\files_for_tests\files_for_tests_inner', '--re', 'test_file3'],
                         capture_output=True, text=True)
        chdir('clifm')
        print(r"Должно быть: ('clifm\\files_for_tests\\files_for_tests_inner', 'test_file3.txt')",
              '\nполучено в тесте:' + cli_result.stdout[:-1])
        self.assertEqual(r"('clifm\\files_for_tests\\files_for_tests_inner', 'test_file3.txt')", cli_result.stdout[:-1])

    def tearDown(self):
        delete_test_dir_and_files()


if __name__ == '__main__':
    unittest.main()
