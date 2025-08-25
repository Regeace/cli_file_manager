import flet as ft
import os.path
from functions import *


def main(page: ft.Page):
    page.title = 'File Manager'

    def clear_text_field():
        result_field.value = 'Результат'
        result_field.update()

    def pick_file_result(e: ft.FilePickerResultEvent):
        path_field.value = e.files[0].path
        path_field.update()

    def show_counted_files():
        path = path_field.value
        result_field.value = count_files(path) if os.path.isdir(path) else 'Каталог не выбран :('
        result_field.update()

    path_field = ft.TextField(hint_text='Путь к файлу или каталогу', value='')
    result_field = ft.Text(value='Результат')
    file_pick_dialog = ft.FilePicker(on_result=pick_file_result)
    file_pick_button = ft.FilledButton('Выбрать файл',
                                       on_click=lambda _: file_pick_dialog.pick_files(allow_multiple=False))

    count_files_button = ft.FilledButton('Количество файлов', on_click=lambda _: show_counted_files())

    page.overlay.append(file_pick_dialog)

    page.add(
        ft.Row(controls=[ft.Container(content=ft.Column(controls=[path_field, file_pick_button, count_files_button])), result_field])
    )


ft.app(main)
