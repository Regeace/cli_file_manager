import flet as ft
import sys
from io import StringIO
from functions import *

'''Различные переменные, используемые для отрисовки интерфейса'''
border_color = 'blue'
buttons_border_style = ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=10))
result_field_default_value = '<- Укажите/выберите адрес файла или каталога и нажмите кнопку интересующей вас опции'
date_tooltip = '''Добавит дату создания файла к имени файла (если выбран конкретный файл)
или к именам всех файлов в выбранном каталоге (если включена опция `Включая вложенные`,
то изменения будут применены ко всем файлам во вложенных каталогах)'''


class PrimaryButton(ft.FilledButton):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.style = buttons_border_style
        self.width = 150


def clear_path_field():
    path_field.value = ''
    path_field.update()


def clear_result_field():
    result_field.value = result_field_default_value
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
    if delete_button_switch.value:
        delete_files_button.disabled = False
        delete_files_button.bgcolor = ft.Colors.RED
    else:
        delete_files_button.disabled = True
        delete_files_button.bgcolor = ft.Colors.GREY_300
    delete_files_button.update()


def show_gui_readme(_=None):
    with open('gui_readme.md', 'r', encoding='utf-8') as readme:
        for line in readme:
            print(line[:-1])


def show_result(magic_word):
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
    if magic_word == 'date' and add_date_recursive.value == True:
        magic_words[magic_word](path_field.value, recursive=True)
    elif magic_word == 'find':
        magic_words[magic_word](path_field.value, find_files_textfield.value)
    else:
        magic_words[magic_word](path_field.value)
    sys.stdout = tmp_stdout
    result_field.value = result.getvalue()
    StringIO().close()

    result_field.update()


'''Текстовые поля, кнопки выбора файла, каталога, очистки текстовых полей'''
path_field = ft.TextField(hint_text='Путь к файлу или каталогу',
                          value='',
                          border_color=border_color)
result_field = ft.Text(value=result_field_default_value)
result_field_container = ft.Column(controls=[result_field],
                                   scroll=ft.ScrollMode.AUTO,
                                   expand=1)
clear_path_button = ft.OutlinedButton('Очистить поле адреса',
                                      style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=10),
                                                           side=ft.BorderSide(1, border_color)),
                                      on_click=lambda _: clear_path_field())
clear_result_button = ft.OutlinedButton('Очистить поле',
                                        width=150,
                                        style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=10),
                                                             side=ft.BorderSide(1, border_color)),
                                        on_click=lambda _: clear_result_field())
file_pick_dialog = ft.FilePicker(on_result=pick_file_result)
file_pick_button = PrimaryButton('Выбрать файл',
                                 on_click=lambda _: file_pick_dialog.pick_files(allow_multiple=False))
catalog_pick_dialog = ft.FilePicker(on_result=pick_catalog_result)
catalog_pick_button = PrimaryButton('Выбрать каталог',
                                    on_click=lambda _: catalog_pick_dialog.get_directory_path())
show_help_button = PrimaryButton('Инструкция',
                                 on_click=lambda _: show_result('show_gui_readme'))

'''Кнопки и другие элементы функционала приложения'''
count_files_button = PrimaryButton('Количество файлов',
                                   on_click=lambda _: show_result('count'))
get_size_button = PrimaryButton('Размер файлов',
                                on_click=lambda _: show_result('size'))
copy_file_button = PrimaryButton('Копировать файл',
                                 on_click=lambda _: show_result('copy'))
add_date_recursive = ft.Checkbox(label='Включая вложенные',
                                 border_side=ft.BorderSide(2, border_color))
add_date_button = PrimaryButton('Добавить дату',
                                tooltip=date_tooltip,
                                on_click=lambda _: show_result('date'))
find_files_textfield = ft.TextField(hint_text='Выражение для поиска файлов',
                                    value='',
                                    border_color=border_color)
find_files_button = PrimaryButton('Поиск файлов',
                                  style=buttons_border_style,
                                  on_click=lambda _: show_result('find'))
delete_button_switch = ft.Switch(label='Включить кнопку удаления файлов',
                                 on_change=lambda _: enable_delete_button())
delete_files_button = PrimaryButton('Удалить файлы',
                                    style=buttons_border_style,
                                    on_click=lambda _: show_result('delete'),
                                    disabled=True)

'''Расположение элементов интерфейса
       Ряд из 2 колонок
       Левая:               Правая:
       Поле адреса          Поле результата
       Кнопки функционала   Кнопка вызова readme
'''

'''Структурные элементы интерфейса'''
pick_entry_container = ft.Container(content=ft.Row(controls=[file_pick_button,
                                                             catalog_pick_button]))
path_container = ft.Container(content=ft.Column(
    controls=[path_field,
              ft.Row(controls=[pick_entry_container,
                               clear_path_button],
                     alignment=ft.MainAxisAlignment.END)]))
find_files_container = ft.Container(content=ft.Row(controls=[find_files_textfield,
                                                             find_files_button],
                                                   alignment=ft.MainAxisAlignment.SPACE_BETWEEN))
add_date_container = ft.Container(content=ft.Row(controls=[add_date_recursive,
                                                           add_date_button],
                                                 alignment=ft.MainAxisAlignment.SPACE_BETWEEN))
delete_files_container = ft.Container(content=ft.Column(controls=[delete_button_switch,
                                                                  delete_files_button]))
right_part_buttons_container = ft.Row(controls=[clear_result_button,
                                                show_help_button],
                                      alignment=ft.MainAxisAlignment.START,
                                      spacing=90)
left = ft.Container(
    content=ft.Column(
        controls=[path_container,
                  count_files_button,
                  get_size_button,
                  copy_file_button,
                  find_files_container,
                  add_date_container,
                  delete_files_container],
        horizontal_alignment=ft.CrossAxisAlignment.END,
        spacing=15),
    width=490,
    height=500)
right = ft.Container(content=ft.Column(
    controls=[ft.Text(value='Результат:', weight=ft.FontWeight.BOLD),
              result_field_container,
              right_part_buttons_container]),
    width=400,
    height=500,
    expand=1)


def main(page: ft.Page):
    page.title = 'File Manager'
    page.scroll = ft.ScrollMode.AUTO
    page.window.left = 400
    page.window.top = 150
    page.window.min_height = 560
    page.window.min_width = 1000
    page.window.width = 1000
    page.window.height = 580

    page.overlay.append(file_pick_dialog)
    page.overlay.append(catalog_pick_dialog)

    page.add(ft.Row(controls=[left, right],
                    spacing=50,
                    vertical_alignment=ft.CrossAxisAlignment.START))


ft.app(main)
