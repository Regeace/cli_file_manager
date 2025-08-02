import os
from cli_functions import make_file


def make_test_dir_and_files():
    """Создаёт папки с файлами для тестовых задач."""
    os.mkdir('files_for_tests')
    os.chdir('files_for_tests')
    [make_file(f'test_file{i}.txt') for i in range(1, 4)]
    os.mkdir('files_for_tests_inner')
    os.chdir('files_for_tests_inner')
    [make_file(f'test_file{i}.txt') for i in range(1, 4)]