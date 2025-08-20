import unittest
import os.path
from os import chdir
from sys import executable
from subprocess import run
from _utils import make_test_dir_and_files, delete_test_dir_and_files

'''При некорректной работе тестов во время вывода кириллицы из stdout (на Windows) заменить в locale кодировку на cp65001'''


class TestCli(unittest.TestCase):
    def setUp(self):
        make_test_dir_and_files()

    def test_cli_valid_expressions(self):
        test_cases = [
            ('count', os.path.normcase('clifm/files_for_tests'), '6'),
            (
            'date', os.path.normcase('clifm/files_for_tests'), 'К именам файлов в каталоге добавлена дата их создания'),
            ('copy', os.path.normcase('clifm/files_for_tests/files_for_tests_inner/test_file1.txt'),
             'Создана копия файла')
        ]

        for magic_word, name_path, answer in test_cases:
            chdir('..')
            with self.subTest(magic_word=magic_word, name_path=name_path, answer=answer):
                cli_result = run([executable, 'cli_file_manager.py', magic_word, name_path], capture_output=True,
                                 text=True)
                # print(f'Должно быть: {answer},\nполучено в тесте: {cli_result.stdout[:-1]}\n')
                self.assertEqual(answer, cli_result.stdout[:-1])
                self.assertEqual(cli_result.returncode, 0)
            chdir('clifm')

    def test_cli_valid_expressions_long(self):
        """"Проверяет работу программы CLI при использовании 4 слов в написании команды"""
        chdir('..')
        path = os.path.normcase('clifm/files_for_tests/files_for_tests_inner')
        cli_result = run([executable, 'cli_file_manager.py', 'find',
                          path, '--re', 'test_file3'],
                         capture_output=True, text=True)
        chdir('clifm')
        # print(r"Должно быть: ('clifm\\files_for_tests\\files_for_tests_inner', 'test_file3.txt')",
        #       '\nполучено в тесте:' + cli_result.stdout[:-1])
        self.assertEqual(str((f'{path}', 'test_file3.txt')), cli_result.stdout[:-1])

    def test_cli_invalid_expressions(self):
        """Проверка некорректного ввода magic_phrase (первого слова)"""
        test_cases = [
            ('five', os.path.normcase('clifm/files_for_tests')),
            ('', os.path.normcase('clifm/files_for_tests')),
            ('', '')
        ]

        for magic_word, name_path in test_cases:
            chdir('..')
            with self.subTest(magic_word=magic_word, name_path=name_path):
                cli_result = run([executable, 'cli_file_manager.py', magic_word, name_path],
                                 capture_output=True, text=True)
                self.assertEqual(cli_result.returncode, 2)
            chdir('clifm')

    def test_cli_invalid_expressions_second(self):
        """Проверка некорректного ввода name (второе слово)"""
        test_cases = [
            ('copy', '5', 'Копирование несуществующего файла'),
            ('date', '5', 'Изменить имя невозможно. Каталог или файл не существует'),
            ('size', '5', 'Невозможно посчитать размер. Каталог или файл не существует'),
            ('count', '', 'Невозможно посчитать файлы. Такой каталог не найден')
        ]

        for magic_word, name_path, answer in test_cases:
            chdir('..')
            with self.subTest(magic_word=magic_word, name_path=name_path, answer=answer):
                cli_result = run([executable, 'cli_file_manager.py', magic_word, name_path],
                                 capture_output=True, text=True)
                # print(f'Должно быть: {answer},\nполучено в тесте: {cli_result.stdout[:-1]}\n')
                self.assertEqual(answer, cli_result.stdout[:-1])
                self.assertEqual(cli_result.returncode, 0)
            chdir('clifm')

    def tearDown(self):
        delete_test_dir_and_files()


if __name__ == '__main__':
    unittest.main()
