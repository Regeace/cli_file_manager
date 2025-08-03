import argparse
import clifm

magic_words = {
    'copy': clifm.copy_file,
    'count': clifm.count_files,
    'delete': clifm.delete_file_or_catalog,
    'find': clifm.find_files,
    'show': clifm.show_help,
    'make': clifm.make_file
}


def main():
    parser = argparse.ArgumentParser(prog='clifm',
                                     description='Небольшой файловый менеджер для консоли',
                                     epilog='Для расширенной помощи дополнительно введите: python cli_file_manager.py show help')
    parser.add_argument('magic_phrase', type=str, choices=magic_words.keys(),
                        help='Команда взаимодействия с файлами и каталогами')
    parser.add_argument('name', type=str, help='Имя файла или каталога')
    parser.add_argument('-a', '--additional_var', type=str, help='Регулярное выражение для поиска')

    args = parser.parse_args()

    magic_words[args.magic_phrase](args.name)


if __name__ == '__main__':
    main()
