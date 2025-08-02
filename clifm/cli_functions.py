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