import os
from cli_functions import make_file, delete_file_or_catalog


def make_test_dir_and_files():
    """
    Создаёт папки с файлами для тестовых задач.
    Структура вида:
    files_for_tests
        files_for_tests_inner
            test_file1.txt
            test_file2.txt
            test_file3.txt
        test_file1.txt
        test_file2.txt
        test_file3.txt
    """
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
    os.chdir('..')

def delete_test_dir_and_files():
    if os.path.exists('files_for_tests'):
        delete_file_or_catalog('files_for_tests')
    else:
        print('Удаление невозможно. Каталог не создан')
