"""Диапазон адресов и дамп памяти данных в формате CSV.

Дамп содержит заголовок и по одной строке на ячейку:

    address,value
    10,5
    11,17
"""

import csv
from pathlib import Path

from .errors import InterpreterError

RANGE_SEPARATOR = ":"
HEADER = ("address", "value")


def parse_range(text, size):
    """Разобрать диапазон адресов вида НАЧАЛО:КОНЕЦ (обе границы входят).

    :param text: строка диапазона, например 10:27.
    :param size: число ячеек памяти данных.
    :returns: пара (начало, конец).
    :raises InterpreterError: если диапазон записан неверно или выходит
        за пределы памяти.
    """
    parts = text.split(RANGE_SEPARATOR)
    if len(parts) != len(HEADER) or not all(p.isdigit() for p in parts):
        raise InterpreterError(
            f"диапазон адресов должен иметь вид НАЧАЛО:КОНЕЦ, "
            f"получено: {text!r}"
        )
    start, end = int(parts[0]), int(parts[1])
    if start > end:
        raise InterpreterError(f"начало диапазона {start} больше конца {end}")
    if end >= size:
        raise InterpreterError(
            f"конец диапазона {end} вне памяти данных (0..{size - 1})"
        )
    return start, end


def write_dump(path, data, start, end):
    """Записать ячейки памяти данных с адресами start..end в CSV.

    Каталог для файла создаётся, если его нет.

    :param path: путь к файлу дампа.
    :param data: память данных (список значений).
    :param start: первый адрес диапазона.
    :param end: последний адрес диапазона (входит в дамп).
    :raises OSError: если файл не удалось записать.
    """
    target = Path(path)
    target.parent.mkdir(parents=True, exist_ok=True)
    with target.open("w", encoding="utf-8", newline="") as file:
        writer = csv.writer(file, lineterminator="\n")
        writer.writerow(HEADER)
        for address in range(start, end + 1):
            writer.writerow((address, data[address]))
