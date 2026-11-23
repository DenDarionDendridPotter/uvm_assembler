"""Ассемблер УВМ: перевод программы на языке JSON в машинный код."""

import argparse
import sys
from pathlib import Path

from .encoder import encode_instruction, encode_program, format_bytes
from .errors import AssemblerError
from .parser import load_program

EXIT_OK = 0
EXIT_ASSEMBLER_ERROR = 1
EXIT_OUTPUT_ERROR = 2


def parse_args(argv=None):
    """Разобрать аргументы командной строки ассемблера.

    :param argv: список аргументов, по умолчанию sys.argv[1:].
    :returns: пространство имён с полями source, output, test и ir.
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
        help="режим тестирования: вывести машинный код каждой команды",
    )
    parser.add_argument(
        "--ir",
        action="store_true",
        help=(
            "режим этапа 1: только перевести программу в промежуточное "
            "представление и вывести поля и значения, без машинного кода"
        ),
    )
    return parser.parse_args(argv)


def print_program(program):
    """Вывести промежуточное представление в формате полей и значений.

    :param program: список команд Instruction.
    """
    for instruction in program:
        print(instruction)


def print_bytes(program):
    """Вывести машинный код каждой команды в байтовом формате.

    :param program: список команд Instruction.
    """
    for instruction in program:
        print(format_bytes(encode_instruction(instruction)))


def write_binary(path, code):
    """Записать машинный код в двоичный файл.

    Каталог для файла создаётся, если его нет.

    :param path: путь к двоичному файлу-результату.
    :param code: байты программы.
    :raises OSError: если файл не удалось записать.
    """
    target = Path(path)
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_bytes(code)


def main(argv=None):
    """Ассемблировать программу и записать машинный код в файл.

    :param argv: список аргументов командной строки.
    :returns: код завершения программы.
    """
    args = parse_args(argv)
    try:
        program = load_program(args.source)
    except AssemblerError as error:
        print(f"ошибка ассемблера: {error}", file=sys.stderr)
        return EXIT_ASSEMBLER_ERROR
    if args.ir:
        print_program(program)
        print(f"разобрано команд: {len(program)}")
        return EXIT_OK
    code = encode_program(program)
    try:
        write_binary(args.output, code)
    except OSError as error:
        print(f"ошибка записи {args.output}: {error}", file=sys.stderr)
        return EXIT_OUTPUT_ERROR
    if args.test:
        print_bytes(program)
    print(f"ассемблировано команд: {len(program)} ({len(code)} байт)")
    return EXIT_OK


if __name__ == "__main__":
    sys.exit(main())
