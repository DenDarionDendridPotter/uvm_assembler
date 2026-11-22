"""Ассемблер УВМ: перевод программы с языка ассемблера (JSON)."""

import argparse
import sys

from .errors import AssemblerError
from .parser import load_program

EXIT_OK = 0
EXIT_ASSEMBLER_ERROR = 1


def parse_args(argv=None):
    """Разобрать аргументы командной строки ассемблера.

    :param argv: список аргументов, по умолчанию sys.argv[1:].
    :returns: пространство имён с полями source, output и test.
    """
    parser = argparse.ArgumentParser(
        prog="asm",
        description="Ассемблер учебной виртуальной машины (вариант 28)",
    )
    parser.add_argument("source", help="путь к программе на языке JSON")
    parser.add_argument("output", help="путь к двоичному файлу-результату")
    parser.add_argument(
        "-t",
        "--test",
        action="store_true",
        help="режим тестирования: вывести промежуточное представление",
    )
    return parser.parse_args(argv)


def print_program(program):
    """Вывести промежуточное представление в формате полей и значений.

    :param program: список команд Instruction.
    """
    for instruction in program:
        print(instruction)


def main(argv=None):
    """Перевести программу в промежуточное представление.

    :param argv: список аргументов командной строки.
    :returns: код завершения программы.
    """
    args = parse_args(argv)
    try:
        program = load_program(args.source)
    except AssemblerError as error:
        print(f"ошибка ассемблера: {error}", file=sys.stderr)
        return EXIT_ASSEMBLER_ERROR
    if args.test:
        print_program(program)
    print(f"разобрано команд: {len(program)}")
    return EXIT_OK


if __name__ == "__main__":
    sys.exit(main())
