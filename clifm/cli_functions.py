import os
from shutil import copy2, rmtree
from re import search
from datetime import date


def show_help(show_readme_file):
    """Выводит построчно в консоль файл readme.md"""
    with open('README.md', 'r', encoding='utf-8') as readme:
        print()
        for line in readme:
            print(line[:-1])
        print()


def make_file(file_name):
    """Создаёт новый файл."""
    with open(file_name, 'w+', encoding='utf-8') as _:
        pass


def copy_file(file_name):
    """Создаёт копию файла с метаданными."""
    if not os.path.exists(file_name):
        print('Файл не существует')
        return
    if os.path.exists('copy_' + file_name):
        copy2(file_name, 'another_copy_' + file_name)
    else:
        copy2(file_name, 'copy_' + file_name)


def count_files(dir_name):
    """Подсчитывает количество файлов в папке."""
    counter = 0
    for base_dir, current_dir, files in os.walk(dir_name):
        counter += len(files)
    return counter


def delete_file_or_catalog(entry_name):
    """Удаляет папку (с файлами) или файл."""
    if os.path.isfile(entry_name):
        os.remove(entry_name)
    else:
        rmtree(entry_name)


