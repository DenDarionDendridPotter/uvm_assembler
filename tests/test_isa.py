"""Тесты описания системы команд УВМ."""

import unittest

from src.isa import (
    BY_NAME,
    BY_OPCODE,
    LOAD_CONST,
    READ,
    SGN,
    WRITE,
    Instruction,
)


class IsaTest(unittest.TestCase):
    """Проверки таблицы команд по спецификации варианта 28."""

    def test_opcodes_and_sizes(self):
        """Коды операций и размеры совпадают со спецификацией."""
        table = [(spec.opcode, spec.size) for spec in BY_NAME.values()]
        self.assertEqual(table, [(30, 4), (29, 3), (28, 3), (3, 1)])

    def test_operand_ranges(self):
        """Ширина поля B задаёт наибольшее значение операнда."""
        self.assertEqual(LOAD_CONST.max_operand, 2**26 - 1)
        self.assertEqual(READ.max_operand, 2**16 - 1)
        self.assertEqual(WRITE.max_operand, 2**17 - 1)
        self.assertEqual(SGN.max_operand, 0)

    def test_lookup_by_opcode(self):
        """Команду можно найти по коду операции."""
        for spec in BY_NAME.values():
            self.assertIs(BY_OPCODE[spec.opcode], spec)

    def test_format_fields(self):
        """Поля записываются как в тестах спецификации."""
        self.assertEqual(str(Instruction(LOAD_CONST, 847)), "A=30, B=847")
        self.assertEqual(str(Instruction(SGN)), "A=3")


if __name__ == "__main__":
    unittest.main()
