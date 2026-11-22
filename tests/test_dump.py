"""Тесты диапазона адресов и дампа памяти в CSV."""

import csv
import tempfile
import unittest
from pathlib import Path

from src.dump import HEADER, parse_range, write_dump
from src.errors import InterpreterError

SIZE = 100


class DumpTest(unittest.TestCase):
    """Проверки разбора диапазона и записи CSV."""

    def test_parse_range(self):
        """Диапазон НАЧАЛО:КОНЕЦ включает обе границы."""
        self.assertEqual(parse_range("10:27", SIZE), (10, 27))
        self.assertEqual(parse_range("5:5", SIZE), (5, 5))

    def test_bad_ranges(self):
        """Неверные диапазоны дают ошибку."""
        for text in ("10", "10-27", "a:b", "-1:5", "9:3", "0:100", "1:2:3"):
            with self.subTest(text):
                with self.assertRaises(InterpreterError):
                    parse_range(text, SIZE)

    def test_write_dump(self):
        """Дамп содержит заголовок и ячейки диапазона."""
        data = list(range(SIZE))
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "dump" / "memory.csv"
            write_dump(path, data, 3, 5)
            with path.open(encoding="utf-8", newline="") as file:
                rows = list(csv.reader(file))
        self.assertEqual(rows[0], list(HEADER))
        self.assertEqual(rows[1:], [["3", "3"], ["4", "4"], ["5", "5"]])


if __name__ == "__main__":
    unittest.main()
