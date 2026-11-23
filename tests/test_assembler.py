"""Тесты запуска ассемблера из командной строки."""

import contextlib
import io
import tempfile
import unittest
from pathlib import Path

from src.assembler import EXIT_ASSEMBLER_ERROR, EXIT_OK, EXIT_OUTPUT_ERROR
from src.main import EXIT_USAGE, main

PROJECT = Path(__file__).resolve().parent.parent
SPEC = str(PROJECT / "programs" / "spec_tests.json")
SPEC_LINES = [
    "0xFE, 0x69, 0x00, 0x00",
    "0xDD, 0x69, 0x00",
    "0x3C, 0x57, 0x00",
    "0x03",
]
SPEC_FIELDS = ["A=30, B=847", "A=29, B=846", "A=28, B=697", "A=3"]
SPEC_CODE = bytes.fromhex("FE690000DD69003C570003")


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

    def setUp(self):
        """Создать временный каталог для двоичных файлов."""
        self.directory = tempfile.TemporaryDirectory()
        self.output = Path(self.directory.name) / "sub" / "program.bin"

    def tearDown(self):
        """Удалить временный каталог."""
        self.directory.cleanup()

    def test_test_mode_prints_bytes(self):
        """В режиме тестирования выводятся байты, как в спецификации."""
        code, out, _ = run(["asm", SPEC, str(self.output), "--test"])
        self.assertEqual(code, EXIT_OK)
        self.assertEqual(out.splitlines()[:len(SPEC_LINES)], SPEC_LINES)

    def test_ir_mode_prints_fields(self):
        """Ключ --ir выводит поля и значения, как в спецификации."""
        code, out, _ = run(["asm", SPEC, str(self.output), "--ir"])
        self.assertEqual(code, EXIT_OK)
        self.assertEqual(out.splitlines()[:len(SPEC_FIELDS)], SPEC_FIELDS)

    def test_binary_file(self):
        """Двоичный файл содержит все тестовые последовательности."""
        run(["asm", SPEC, str(self.output)])
        self.assertEqual(self.output.read_bytes(), SPEC_CODE)

    def test_prints_command_count(self):
        """На экран выводится число ассемблированных команд."""
        _, out, _ = run(["asm", SPEC, str(self.output)])
        self.assertEqual(out.strip(), "ассемблировано команд: 4 (11 байт)")

    def test_output_error(self):
        """Ошибка записи файла даёт код 2."""
        directory = self.directory.name
        code, _, err = run(["asm", SPEC, directory])
        self.assertEqual(code, EXIT_OUTPUT_ERROR)
        self.assertIn("ошибка записи", err)

    def test_error_exit_code(self):
        """Ошибка в программе даёт код 1 и сообщение в stderr."""
        bad = str(PROJECT / "programs" / "errors" / "unknown_command.json")
        code, _, err = run(["asm", bad, str(self.output)])
        self.assertEqual(code, EXIT_ASSEMBLER_ERROR)
        self.assertIn("неизвестная команда", err)

    def test_unknown_tool(self):
        """Без имени программы выводится подсказка."""
        code, _, err = run(["nothing"])
        self.assertEqual(code, EXIT_USAGE)
        self.assertIn("использование", err)


if __name__ == "__main__":
    unittest.main()
