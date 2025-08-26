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

    def show_result(madic_word):
        """Вызывает функцию из functions.py и показывает результат."""
        magic_words = {
            'copy': copy_file,
            'count': count_files,
            'date': add_date_to_name,
            'delete': delete_file_or_catalog,
            'find': find_files,
            'size': show_size
        }

        entry_path = path_field.value

        '''Сохранение stdout в переменную, вызов функции, возврат к стандартному потоку вывода'''
        tmp_stdout = sys.stdout
        result = StringIO()
        sys.stdout = result
        magic_words[madic_word](entry_path)
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

    '''Кнопки функционала приложения'''
    count_files_button = ft.FilledButton('Количество файлов', on_click=lambda _: show_result('count'))

    page.overlay.append(file_pick_dialog)
    page.overlay.append(catalog_pick_dialog)

    page.add(
        ft.Row(controls=[ft.Container(
            content=ft.Column(
                controls=[path_field, file_pick_button, catalog_pick_button, clear_path_button, count_files_button])),
            ft.Container(content=ft.Column(controls=[ft.Text(value='Результат:'), result_field, clear_result_button]))])
    )


ft.app(main)
