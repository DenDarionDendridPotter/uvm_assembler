"""Тесты перевода промежуточного представления в машинный код."""

import unittest

from src.encoder import encode_instruction, encode_program, format_bytes
from src.isa import LOAD_CONST, READ, SGN, WRITE, Instruction

SPEC_TESTS = [
    (Instruction(LOAD_CONST, 847), "0xFE, 0x69, 0x00, 0x00"),
    (Instruction(READ, 846), "0xDD, 0x69, 0x00"),
    (Instruction(WRITE, 697), "0x3C, 0x57, 0x00"),
    (Instruction(SGN), "0x03"),
]


class EncoderTest(unittest.TestCase):
    """Проверки машинного кода по тестам спецификации."""

    def test_spec_bytes(self):
        """Каждая команда даёт байты из спецификации."""
        for instruction, expected in SPEC_TESTS:
            with self.subTest(str(instruction)):
                code = encode_instruction(instruction)
                self.assertEqual(format_bytes(code), expected)

    def test_size(self):
        """Число байт равно размеру команды."""
        for instruction, _ in SPEC_TESTS:
            code = encode_instruction(instruction)
            self.assertEqual(len(code), instruction.spec.size)

    def test_max_operands(self):
        """Наибольшие операнды занимают поле B целиком."""
        code = encode_instruction(Instruction(LOAD_CONST, 2**26 - 1))
        self.assertEqual(code, bytes.fromhex("FEFFFF7F"))
        code = encode_instruction(Instruction(WRITE, 2**17 - 1))
        self.assertEqual(code, bytes.fromhex("FCFF3F"))

    def test_program(self):
        """Программа это байты команд подряд."""
        program = [instruction for instruction, _ in SPEC_TESTS]
        expected = bytes.fromhex("FE690000DD69003C570003")
        self.assertEqual(encode_program(program), expected)


if __name__ == "__main__":
    unittest.main()
