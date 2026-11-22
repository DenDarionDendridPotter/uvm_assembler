"""Точка входа: выбор программы по первому аргументу.

Запуск ассемблера: python -m src.main asm программа.json программа.bin
Запуск интерпретатора: python -m src.main vm программа.bin дамп.csv 0:9
"""

import sys

from . import assembler, interpreter

TOOLS = {"asm": assembler.main, "vm": interpreter.main}
EXIT_USAGE = 1
USAGE = (
    "использование: run.sh asm|vm аргументы... "
    "(подробнее: run.sh asm -h, run.sh vm -h)"
)


def main(argv=None):
    """Запустить ассемблер или интерпретатор.

    :param argv: аргументы командной строки; первый выбирает программу.
    :returns: код завершения программы.
    """
    argv = sys.argv[1:] if argv is None else argv
    if not argv or argv[0] not in TOOLS:
        print(USAGE, file=sys.stderr)
        return EXIT_USAGE
    return TOOLS[argv[0]](argv[1:])


if __name__ == "__main__":
    sys.exit(main())
