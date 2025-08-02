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


def find_files(directory, re_expr):
    """Возвращает список из пар (папка, файл) согласно регулярному выражению re_expr в каталоге и всех подкаталогах, начиная с directory."""
    files = []
    if not os.path.exists(directory):
        print('Каталог не существует')
        return

    for base_dir, current_dir, checking_files in os.walk(directory):
        for elem in checking_files:
            if base_dir:
                if search(elem, re_expr):
                    files.append((base_dir, elem))
            else:
                if search(re_expr, elem):
                    files.append((current_dir, elem))

    if len(files) == 0:
        print('Файлы не найдены')
        return
    return files


def add_date_to_name(entry_name, recursive=False):
    """Добавляет к названию файла/файлов дату их создания."""
    if not os.path.exists(entry_name):
        print('Каталог или файл не существует')
        return

    if os.path.isfile(entry_name):
        # date.fromtimestamp() преобразует время в строку 'YYYY-MM-DD'
        # os.path.getctime() возвращает время создания файла для Windows
        name = os.path.basename(entry_name)
        name_with_date = f'{name[:name.rfind('.')]}_{date.fromtimestamp(os.path.getctime(entry_name))}{name[name.rfind('.'):]}'
        os.rename(entry_name, name_with_date)
    else:
        for entry in os.scandir(entry_name):
            if entry.is_file():
                name = os.path.basename(entry)
                name_with_date = f'{name[:name.rfind('.')]}_{date.fromtimestamp(os.path.getctime(entry_name))}{name[name.rfind('.'):]}'
                os.rename(entry, os.path.join(entry_name, name_with_date))
            elif entry.is_dir() and recursive:
                add_date_to_name(entry, recursive=True)


