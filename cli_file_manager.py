import argparse
import clifm

magic_words = {
    'copy': clifm.copy_file,
    'count': clifm.count_files,
    'date': clifm.add_date_to_name,
    'delete': clifm.delete_file_or_catalog,
    'find': clifm.find_files,
    'make': clifm.make_file,
    'show': clifm.show_help,
    'size': clifm.show_size
}


def main():
    parser = argparse.ArgumentParser(prog='clifm',
                                     description='Небольшой файловый менеджер для консоли',
                                     epilog='Для ознакомления с возможными командами введите: python cli_file_manager.py show help')
    parser.add_argument('magic_phrase', type=str, choices=magic_words.keys(),
                        help='Команда взаимодействия с файлами и каталогами')
    parser.add_argument('name', type=str, help='Имя файла или каталога, путь к файлу или каталогу')
    parser.add_argument('--re', type=str, default='.', help='Подстрока или регулярное выражение для поиска файлов')
    parser.add_argument('--recursive', default=False, action='store_true',
                        help='Дата создания файла прибавляется к файлам во вложенных каталогах')

    args = parser.parse_args()

    if args.magic_phrase == 'date':
        magic_words[args.magic_phrase](args.name, args.recursive)
    elif args.magic_phrase == 'find':
        magic_words[args.magic_phrase](args.name, args.re)
    else:
        magic_words[args.magic_phrase](args.name)


if __name__ == '__main__':
    main()
