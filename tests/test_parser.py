"""Тесты разбора языка ассемблера в промежуточное представление."""

import tempfile
import unittest
from pathlib import Path

from src.errors import AssemblerError
from src.isa import LOAD_CONST, READ, SGN, WRITE, Instruction
from src.parser import load_program, parse_program

PROJECT = Path(__file__).resolve().parent.parent
PROGRAMS = PROJECT / "programs"
SPEC_FIELDS = [
    [("A", 30), ("B", 847)],
    [("A", 29), ("B", 846)],
    [("A", 28), ("B", 697)],
    [("A", 3)],
]


class ParserTest(unittest.TestCase):
    """Проверки перевода JSON в список команд."""

    def test_spec_tests_fields(self):
        """Программа тестов спецификации даёт те же поля и значения."""
        program = load_program(PROGRAMS / "spec_tests.json")
        self.assertEqual([item.fields() for item in program], SPEC_FIELDS)

    def test_all_commands(self):
        """Поддержаны все четыре команды спецификации."""
        text = (
            '[{"op": "load_const", "constant": 1},'
            ' {"op": "read", "offset": 2},'
            ' {"op": "write", "address": 3}, {"op": "sgn"}]'
        )
        expected = [
            Instruction(LOAD_CONST, 1),
            Instruction(READ, 2),
            Instruction(WRITE, 3),
            Instruction(SGN),
        ]
        self.assertEqual(parse_program(text), expected)

    def test_comment_is_ignored(self):
        """Поле comment не влияет на команду."""
        program = parse_program('[{"op": "sgn", "comment": "знак"}]')
        self.assertEqual(program, [Instruction(SGN)])

    def test_operand_limits(self):
        """Наибольшие значения операндов допустимы."""
        text = (
            '[{"op": "load_const", "constant": 67108863},'
            ' {"op": "write", "address": 0}]'
        )
        program = parse_program(text)
        self.assertEqual(program[0].operand, LOAD_CONST.max_operand)

    def test_error_examples(self):
        """Каждый пример из programs/errors даёт ошибку ассемблера."""
        files = sorted((PROGRAMS / "errors").glob("*.json"))
        self.assertTrue(files)
        for path in files:
            with self.subTest(path.name):
                with self.assertRaises(AssemblerError):
                    load_program(path)

    def test_error_mentions_command_number(self):
        """В сообщении об ошибке указан номер команды."""
        text = '[{"op": "sgn"}, {"op": "read", "offset": 70000}]'
        with self.assertRaisesRegex(AssemblerError, "команда 2"):
            parse_program(text)

    def test_bool_is_not_number(self):
        """Логическое значение не принимается вместо числа."""
        with self.assertRaises(AssemblerError):
            parse_program('[{"op": "load_const", "constant": true}]')

    def test_missing_file(self):
        """Отсутствующий файл даёт понятную ошибку."""
        with tempfile.TemporaryDirectory() as directory:
            with self.assertRaisesRegex(AssemblerError, "не найден"):
                load_program(Path(directory) / "nothing.json")


if __name__ == "__main__":
    unittest.main()
