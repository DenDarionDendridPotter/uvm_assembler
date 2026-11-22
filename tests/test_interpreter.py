"""Тесты запуска интерпретатора из командной строки."""

import csv
import tempfile
import unittest
from pathlib import Path

from src.interpreter import EXIT_INPUT_ERROR, EXIT_OK, EXIT_RUNTIME_ERROR
from tests.test_assembler import run
from tests.test_parser import PROGRAMS

COPY = str(PROGRAMS / "stage3" / "copy_array.json")
BAD_READ = str(PROGRAMS / "stage3" / "bad_read_address.json")


class InterpreterCliTest(unittest.TestCase):
    """Проверки полного цикла: ассемблер, интерпретатор, дамп."""

    def setUp(self):
        """Создать временный каталог для файлов."""
        self.directory = tempfile.TemporaryDirectory()
        self.path = Path(self.directory.name)

    def tearDown(self):
        """Удалить временный каталог."""
        self.directory.cleanup()

    def assemble(self, source):
        """Ассемблировать программу во временный каталог.

        :param source: путь к программе на языке ассемблера.
        :returns: путь к двоичному файлу.
        """
        binary = str(self.path / "program.bin")
        run(["asm", source, binary])
        return binary

    def test_copy_array_dump(self):
        """Дамп после копирования содержит обе копии массива."""
        dump = self.path / "dump.csv"
        code, out, _ = run(["vm", self.assemble(COPY), str(dump), "10:27"])
        self.assertEqual(code, EXIT_OK)
        self.assertIn("выполнено команд: 40", out)
        with dump.open(encoding="utf-8", newline="") as file:
            values = {int(a): int(v) for a, v in list(csv.reader(file))[1:]}
        for offset in range(8):
            self.assertEqual(values[10 + offset], values[20 + offset])
        self.assertEqual(values[17], 2**26 - 1)

    def test_runtime_error(self):
        """Ошибка выполнения даёт код 2."""
        args = ["vm", self.assemble(BAD_READ), str(self.path / "d.csv"), "0:1"]
        code, _, err = run(args)
        self.assertEqual(code, EXIT_RUNTIME_ERROR)
        self.assertIn("вне памяти", err)

    def test_input_errors(self):
        """Нет файла или неверный диапазон: код 1."""
        dump = str(self.path / "d.csv")
        missing = str(self.path / "nothing.bin")
        self.assertEqual(run(["vm", missing, dump, "0:1"])[0], EXIT_INPUT_ERROR)
        binary = self.assemble(COPY)
        self.assertEqual(run(["vm", binary, dump, "5"])[0], EXIT_INPUT_ERROR)


if __name__ == "__main__":
    unittest.main()
