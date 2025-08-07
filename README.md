# cli_file_manager
Небольшой файловый менеджер для работы из командной строки

Позволяет копировать файлы, удалять каталоги/файлы,
подсчитывать количество файлов и размер каталога и его содержимого,
осуществлять поиск файлов в каталоге.

Базовая помощь вызывается командой:
    python cli_file_manager.py -h/--help

Вызвать файл 'readme' можно командой:
    python cli_file_manager.py show help

Создать файл в текущей папке по имени или по адресу (абсолютному или относительному):
    python cli_file_manager.py make <file_name/file_path>

Скопировать файл. Копирование происходит в тот же каталог.
Если копия уже существует, создаст ещё одну копию:
    python cli_file_manager.py copy <file_name/file_path>

Удалить файл или каталог:
    python cli_file_manager.py delete <file_or_directory_name/file_or_directory_path>

Команда, позволяющая подсчитать общее количество файлов в каталоге (в том числе и во вложенных):
    python cli_file_manager.py count <directory_name/directory_path>

Команда, позволяющая найти все подходящие файлы в папке (в том числе во вложенных) 
по фильтру подстроки или регулярного выражения.
Поиск ведётся по всему имени файла на возможность вхождения подстроки.
Возвращает список из пар (каталог, файл) согласно подстроке или регулярному выражению expression:
    python cli_file_manager.py find <directory_name/directory_path> --re <expression>

Добавить дату создания к имени файла, ко всем файлам, если указан каталог. 
Если с ключом --recursive, то во всех вложенных каталогах:
    python cli_file_manager.py <file_name/file_path>
    python cli_file_manager.py <file_or_directory_name/file_or_directory_path>
    python cli_file_manager.py <file_or_directory_name/file_or_directory_path> --recursive

Выводит размер каталогов и файлов, начиная с переданного в следующей команде:
    python cli_file_manager.py <file_or_directory_name/file_or_directory_path> 
