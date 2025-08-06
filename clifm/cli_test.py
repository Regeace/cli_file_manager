import unittest
from sys import executable
from subprocess import run
from functions import *
from _utils import make_test_dir_and_files, delete_test_dir_and_files


class TestCli(unittest.TestCase):
    def setUp(self):
        make_test_dir_and_files()

    def test_cli_valid_expressions(self):
        test_cases = [
            ('count', r'clifm\files_for_tests', 6)
        ]

        for magic_word, name_path, answer in test_cases:
            os.chdir('..')
            with self.subTest(magic_word=magic_word, name_path=name_path):
                cli_result = run([executable, 'cli_file_manager.py', magic_word, name_path], capture_output=True,
                                 text=True)
                print(f'Должно быть: {answer}, получено в тесте: {cli_result.stdout}')
                self.assertEqual(answer, int(cli_result.stdout))
            os.chdir('clifm')

    def tearDown(self):
        delete_test_dir_and_files()


if __name__ == '__main__':
    unittest.main(argv=['', ], exit=False)