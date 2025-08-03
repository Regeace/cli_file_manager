import os
from cli_functions import make_file, delete_file_or_catalog


def make_test_dir_and_files():
    """Создаёт папки с файлами для тестовых задач."""
    if os.path.exists('files_for_tests'):
        print('Тестовый каталог уже создан')
        return

    os.mkdir('files_for_tests')
    os.chdir('files_for_tests')
    [make_file(f'test_file{i}.txt') for i in range(1, 4)]
    os.mkdir('files_for_tests_inner')
    os.chdir('files_for_tests_inner')
    [make_file(f'test_file{i}.txt') for i in range(1, 4)]
    os.chdir('..')


def delete_test_dir_and_files():
    os.chdir('..')
    if os.path.exists('files_for_tests'):
        delete_file_or_catalog('files_for_tests')
    else:
        print('Удаление невозможно. Каталог не создан')
