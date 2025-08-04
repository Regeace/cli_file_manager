# cli_file_manager
Небольшой файловый менеджер для работы из командной строки

Позволяет копировать файлы, удалять каталоги/файлы,
подсчитывать количество файлов и размер каталога и его содержимого,
осуществлять поиск файлов в каталоге.

Базовая помощь вызывается командой
    python cli_file_manager.py -h/--help

Вызвать файл 'readme' можно командой:
    python cli_file_manager.py show help

Создать файл в текущей папке по имени или по адресу (абсолютному или относительному):
    python cli_file_manager.py make <file_name/file_path>

Скопировать файл.
Если копия уже существует, создаст ещё одну копию:
    python cli_file_manager.py copy <file_name/file_path>

Удалить файл или каталог:
    python cli_file_manager.py delete <file_or_directory_name/file_or_directory_path>

Команда, позволяющая подсчитать общее количество файлов в каталоге (в том числе и во вложенных):
    python cli_file_manager.py count <directory_name/directory_path>

Команда, позволяющая найти все подходящие файлы в папке (в том числе вложенные) по фильтру регулярного выражения.
Возвращает список из пар (каталог, файл) согласно регулярному выражению regular_expression:
    python cli_file_manager.py find <directory_name/directory_path> regular_expression

Добавить дату создания к имени файла, ко всем файлам, если указан каталог. 
Если с ключом -r/--recursive, то во всех вложенных каталогах:
    python cli_file_manager.py <file_name/file_path>
    python cli_file_manager.py <file_or_directory_name/file_or_directory_path>
    python cli_file_manager.py <file_or_directory_name/file_or_directory_path> -r/--recursive

Команда, запускающая анализ всех вложенных папок и файлов 
и выводящая информацию о том, насколько большие файлы находятся на уровне вызова:
    python cli_file_manager.py <file_or_directory_name/file_or_directory_path>