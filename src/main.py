"""Точка входа: выбор программы по первому аргументу.

    python -m src.main asm программа.json программа.bin [--test]
"""

import sys

from . import assembler

TOOLS = {"asm": assembler.main}
EXIT_USAGE = 1
USAGE = "использование: run.sh asm аргументы... (подробнее: run.sh asm -h)"


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
