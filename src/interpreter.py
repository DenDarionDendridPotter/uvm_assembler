"""Интерпретатор УВМ: выполнение двоичной программы и дамп памяти."""

import argparse
import sys
from pathlib import Path

from .dump import parse_range, write_dump
from .errors import InterpreterError
from .machine import DATA_SIZE, Machine

EXIT_OK = 0
EXIT_INPUT_ERROR = 1
EXIT_RUNTIME_ERROR = 2


def parse_args(argv=None):
    """Разобрать аргументы командной строки интерпретатора.

    :param argv: список аргументов, по умолчанию sys.argv[1:].
    :returns: пространство имён с полями program, dump и range.
    """
    parser = argparse.ArgumentParser(
        prog="vm",
        description="Интерпретатор учебной виртуальной машины (вариант 28)",
    )
    parser.add_argument("program", help="путь к двоичному файлу программы")
    parser.add_argument("dump", help="путь к файлу дампа памяти (CSV)")
    parser.add_argument(
        "range",
        help="диапазон адресов памяти данных для дампа: НАЧАЛО:КОНЕЦ",
    )
    return parser.parse_args(argv)


def load_binary(path):
    """Прочитать двоичный файл программы.

    :param path: путь к файлу.
    :returns: байты программы.
    :raises InterpreterError: если файл не прочитан.
    """
    try:
        return Path(path).read_bytes()
    except FileNotFoundError:
        raise InterpreterError(f"файл программы не найден: {path}") from None
    except OSError as error:
        message = f"не удалось прочитать {path}: {error}"
        raise InterpreterError(message) from None


def main(argv=None):
    """Выполнить программу и сохранить дамп памяти данных.

    :param argv: список аргументов командной строки.
    :returns: код завершения программы.
    """
    args = parse_args(argv)
    try:
        start, end = parse_range(args.range, DATA_SIZE)
        machine = Machine(load_binary(args.program))
    except InterpreterError as error:
        print(f"ошибка интерпретатора: {error}", file=sys.stderr)
        return EXIT_INPUT_ERROR
    try:
        steps = machine.run()
    except InterpreterError as error:
        print(f"ошибка выполнения: {error}", file=sys.stderr)
        return EXIT_RUNTIME_ERROR
    try:
        write_dump(args.dump, machine.data, start, end)
    except OSError as error:
        print(f"ошибка записи {args.dump}: {error}", file=sys.stderr)
        return EXIT_INPUT_ERROR
    print(f"выполнено команд: {steps}, аккумулятор: {machine.acc}")
    print(f"дамп памяти {start}..{end} записан в {args.dump}")
    return EXIT_OK


if __name__ == "__main__":
    sys.exit(main())
