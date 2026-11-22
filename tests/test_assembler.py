"""Тесты запуска ассемблера из командной строки."""

import contextlib
import io
import unittest
from pathlib import Path

from src.assembler import EXIT_ASSEMBLER_ERROR, EXIT_OK
from src.main import EXIT_USAGE, main

PROJECT = Path(__file__).resolve().parent.parent
SPEC = str(PROJECT / "programs" / "spec_tests.json")
SPEC_LINES = ["A=30, B=847", "A=29, B=846", "A=28, B=697", "A=3"]


def run(argv):
    """Запустить main и перехватить вывод.

    :param argv: аргументы командной строки.
    :returns: кортеж (код завершения, stdout, stderr).
    """
    out, err = io.StringIO(), io.StringIO()
    with contextlib.redirect_stdout(out), contextlib.redirect_stderr(err):
        code = main(argv)
    return code, out.getvalue(), err.getvalue()


class AssemblerCliTest(unittest.TestCase):
    """Проверки кода завершения и вывода ассемблера."""

    def test_test_mode_prints_fields(self):
        """В режиме тестирования выводятся поля, как в спецификации."""
        code, out, _ = run(["asm", SPEC, "out.bin", "--test"])
        self.assertEqual(code, EXIT_OK)
        self.assertEqual(out.splitlines()[:len(SPEC_LINES)], SPEC_LINES)

    def test_error_exit_code(self):
        """Ошибка в программе даёт код 1 и сообщение в stderr."""
        bad = str(PROJECT / "programs" / "errors" / "unknown_command.json")
        code, _, err = run(["asm", bad, "out.bin"])
        self.assertEqual(code, EXIT_ASSEMBLER_ERROR)
        self.assertIn("неизвестная команда", err)

    def test_unknown_tool(self):
        """Без имени программы выводится подсказка."""
        code, _, err = run(["nothing"])
        self.assertEqual(code, EXIT_USAGE)
        self.assertIn("использование", err)


if __name__ == "__main__":
    unittest.main()
