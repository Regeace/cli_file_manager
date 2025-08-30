import flet as ft
import sys
from io import StringIO
from functions import *


def main(page: ft.Page):
    page.title = 'File Manager'

    def clear_path_field():
        path_field.value = ''
        path_field.update()

    def clear_result_field():
        result_field.value = ''
        result_field.update()

    def pick_file_result(e: ft.FilePickerResultEvent):
        """Получает и показывает путь к выбранному файлу."""
        path_field.value = e.files[0].path if e.files else ''
        path_field.update()

    def pick_catalog_result(e: ft.FilePickerResultEvent):
        """Получает и показывает путь к выбранному каталогу."""
        path_field.value = e.path
        path_field.update()

    def enable_delete_button():
        """Включает и выключает кнопку удаления файлов"""
        if delete_button_checkbox.value:
            delete_files_button.disabled = False
            delete_files_button.bgcolor = ft.Colors.RED
        else:
            delete_files_button.disabled = True
            delete_files_button.bgcolor = ft.Colors.GREY_300
        delete_files_button.update()

    def show_gui_readme(_=None):
        with open('gui_readme.txt', 'r', encoding='utf-8') as readme:
            for line in readme:
                print(line[:-1])

    def show_result(madic_word):
        """Вызывает функцию из functions.py и показывает результат."""
        magic_words = {
            'copy': copy_file,
            'count': count_files,
            'date': add_date_to_name,
            'delete': delete_file_or_catalog,
            'find': find_files,
            'size': show_size,
            'show_gui_readme': show_gui_readme
        }

        '''Сохранение stdout в переменную, вызов функции, возврат к стандартному потоку вывода'''
        tmp_stdout = sys.stdout
        result = StringIO()
        sys.stdout = result
        if madic_word == 'date' and add_date_recursive.value == True:
            magic_words[madic_word](path_field.value, recursive=True)
        elif madic_word == 'find':
            magic_words[madic_word](path_field.value, find_files_textfield.value)
        else:
            magic_words[madic_word](path_field.value)
        sys.stdout = tmp_stdout
        result_field.value = result.getvalue()
        StringIO().close()

        result_field.update()

    '''Текстовые поля, кнопки выбора файла, каталога, очистки текстовых полей'''
    path_field = ft.TextField(hint_text='Путь к файлу или каталогу', value='')
    result_field = ft.Text(value='')
    clear_path_button = ft.FilledButton('Очистить поле адреса', on_click=lambda _: clear_path_field())
    clear_result_button = ft.FilledButton('Очистить поле', on_click=lambda _: clear_result_field())
    file_pick_dialog = ft.FilePicker(on_result=pick_file_result)
    file_pick_button = ft.FilledButton('Выбрать файл',
                                       on_click=lambda _: file_pick_dialog.pick_files(allow_multiple=False))
    catalog_pick_dialog = ft.FilePicker(on_result=pick_catalog_result)
    catalog_pick_button = ft.FilledButton('Выбрать каталог',
                                          on_click=lambda _: catalog_pick_dialog.get_directory_path())
    show_help_button = ft.FilledButton('Инструкция', on_click=lambda _: show_result('show_gui_readme'))

    '''Кнопки и другие элементы функционала приложения'''
    count_files_button = ft.FilledButton('Количество файлов', on_click=lambda _: show_result('count'))
    get_size_button = ft.FilledButton('Размер файлов', on_click=lambda _: show_result('size'))
    copy_file_button = ft.FilledButton('Копировать файл', on_click=lambda _: show_result('copy'))
    add_date_recursive = ft.Checkbox(label='Включая вложенные')
    add_date_button = ft.FilledButton('Добавить дату', on_click=lambda _: show_result('date'))
    find_files_textfield = ft.TextField(hint_text='Выражение для поиска файлов', value='')
    find_files_button = ft.FilledButton('Поиск файлов', on_click=lambda _: show_result('find'))
    delete_button_checkbox = ft.Checkbox(label='Включить кнопку удаления файлов',
                                         on_change=lambda _: enable_delete_button())
    delete_files_button = ft.FilledButton('Удалить файлы', on_click=lambda _: show_result('delete'), disabled=True)

    page.overlay.append(file_pick_dialog)
    page.overlay.append(catalog_pick_dialog)

    '''Расположение элементов интерфейса
        Ряд из 2 колонок
        Левая:               Правая:
        Поле адреса          Поле результата
        Кнопки функционала   Кнопка вызова readme
    '''

    '''Структурные элементы интерфейса'''
    pick_entry_container = ft.Container(content=ft.Row(controls=[file_pick_button, catalog_pick_button]))
    path_container = ft.Container(content=ft.Column(
        controls=[path_field, ft.Column(controls=[pick_entry_container, clear_path_button])]))
    find_files_container = ft.Container(content=ft.Column(controls=[find_files_textfield, find_files_button]))
    add_date_container = ft.Container(content=ft.Row(controls=[add_date_recursive, add_date_button]))
    delete_files_container = ft.Container(content=ft.Column(controls=[delete_button_checkbox, delete_files_button]))
    left = ft.Container(
        content=ft.Column(
            controls=[path_container, count_files_button, get_size_button, copy_file_button, find_files_container,
                      add_date_container, delete_files_container]))
    right = ft.Container(content=ft.Column(
        controls=[ft.Text(value='Результат:'), result_field, clear_result_button, show_help_button]))

    page.add(ft.Row(controls=[left, right]))


ft.app(main)
