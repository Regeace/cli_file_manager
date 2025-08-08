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


def make_file(file_name, show_result=True):
    """Создаёт новый файл."""
    with open(file_name, 'w+', encoding='utf-8') as _:
        pass

    if show_result:
        print('Файл создан')


def copy_file(file_name, show_result=True):
    """Создаёт копию файла с метаданными."""
    if not os.path.exists(file_name) or os.path.isdir(file_name):
        print('Копирование несуществующего файла')
        return

    if os.path.isfile(file_name):
        if '\\' not in file_name:
            if os.path.exists('copy_' + file_name):
                copy2(file_name, 'another_copy_' + file_name)
            else:
                copy2(file_name, 'copy_' + file_name)
        else:
            if os.path.exists(f'{os.path.dirname(file_name)}\\copy_{os.path.basename(file_name)}'):
                copy2(file_name, f'{os.path.dirname(file_name)}\\another_copy_{os.path.basename(file_name)}')
            else:
                copy2(file_name, f'{os.path.dirname(file_name)}\\copy_{os.path.basename(file_name)}')

    if show_result:
        print('Создана копия файла')


def count_files(dir_name, show_result=True):
    """Подсчитывает количество файлов в папке."""
    if not os.path.exists(dir_name):
        print('Невозможно посчитать файлы. Такой каталог не найден')
        return

    counter = 0
    for base_dir, current_dir, files in os.walk(dir_name):
        counter += len(files)
    if show_result:
        print(counter)

    return counter


def delete_file_or_catalog(entry_name, show_result=True):
    """Удаляет папку (с файлами) или файл."""
    if os.path.exists(entry_name):
        if os.path.isfile(entry_name):
            os.remove(entry_name)
        else:
            rmtree(entry_name)
    else:
        print('Удалить невозможно. Каталог/файл не существует')
        return

    if show_result:
        print('Каталог/файл удалён')


def find_files(directory, re_expr, show_result=True):
    """Возвращает список из пар (папка, файл) согласно подстроке или регулярному выражению re_expr в каталоге и всех подкаталогах, начиная с directory."""
    files = []
    if not os.path.exists(directory):
        print('Каталог не существует')
        return

    for base_dir, current_dir, checking_files in os.walk(directory):
        for elem in checking_files:
            if base_dir:
                if search(re_expr, elem):
                    files.append((base_dir, elem))
            else:
                if search(re_expr, elem):
                    files.append((current_dir, elem))

    if len(files) == 0:
        print('Файлы не найдены')
    elif len(files) != 0 and show_result:
        print(*files, sep='\n')

    return files


def add_date_to_name(entry_name, recursive=False, show_result=True):
    """Добавляет к названию файла/файлов дату их создания."""
    if not os.path.exists(entry_name):
        print('Изменить имя невозможно. Каталог или файл не существует')
        return

    if os.path.isfile(entry_name):
        '''date.fromtimestamp() преобразует время в строку 'YYYY-MM-DD'
           os.path.getctime() возвращает время создания файла для Windows'''
        name = os.path.basename(entry_name)
        if '\\' not in entry_name:
            name_with_date = f'{name[:name.rfind('.')]}_{date.fromtimestamp(os.path.getctime(entry_name))}{name[name.rfind('.'):]}'
        else:
            name_with_date = f'{os.path.dirname(entry_name)}\\{name[:name.rfind('.')]}_{date.fromtimestamp(os.path.getctime(entry_name))}{name[name.rfind('.'):]}'
        os.rename(entry_name, name_with_date)
    else:
        for entry in os.scandir(entry_name):
            if entry.is_file():
                name = os.path.basename(entry)
                name_with_date = f'{name[:name.rfind('.')]}_{date.fromtimestamp(os.path.getctime(entry_name))}{name[name.rfind('.'):]}'
                os.rename(entry, os.path.join(entry_name, name_with_date))
            elif entry.is_dir() and recursive:
                add_date_to_name(entry, recursive=True, show_result=False)

    if show_result:
        print('К именам файлов в каталоге добавлена дата их создания')


def format_size(num_of_bites):
    """Преобразует количество байтов в читаемый формат kB, MB, GB"""
    for elem in ['', 'k', 'M', 'G']:
        if num_of_bites < 1000:
            if elem == '':
                return f'{num_of_bites} {elem}B'
            else:
                return f'{round(num_of_bites, 1)} {elem}B'
        num_of_bites /= 1000
    return f'{round(num_of_bites, 1)} {elem}B'


def show_size(entry_dir):
    """Показывает размер каталогов, подкаталогов и файлов, размещённых в них."""
    if not os.path.exists(entry_dir):
        print('Невозможно посчитать размер. Каталог или файл не существует')
        return

    dict_of_sizes = {entry_dir: None}

    def get_size(entry_name, show_inner_dir_files=True):
        """Считает размер каталогов, подкаталогов и файлов, размещённых в них."""
        nonlocal dict_of_sizes
        directory_size = 0

        if count_files(entry_name, show_result=False) == 0:
            return 0

        for entry in os.scandir(entry_name):
            if entry.is_file():
                directory_size += os.path.getsize(entry)
                if show_inner_dir_files:
                    dict_of_sizes[entry.name] = os.path.getsize(entry)
            else:
                local_directory_size = 0
                if count_files(entry.path, show_result=False) == 0 and show_inner_dir_files:
                    dict_of_sizes[entry.name] = 0
                else:
                    local_directory_size += get_size(entry.path, show_inner_dir_files=False)
                    directory_size += local_directory_size
                    if show_inner_dir_files:
                        dict_of_sizes[entry.name] = local_directory_size

        return directory_size

    dict_of_sizes[entry_dir] = get_size(entry_dir)
    flag = True
    for key, value in dict_of_sizes.items():
        if flag:
            print(f'{key}    {format_size(value)}')
            flag = False
        else:
            print(f'   - {key}    {format_size(value)}')

    return dict_of_sizes
