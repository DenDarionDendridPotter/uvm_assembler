"""Тесты перевода машинного кода в промежуточное представление."""

import unittest

from src.decoder import decode_instruction, decode_program
from src.encoder import encode_program
from src.errors import InterpreterError
from src.isa import LOAD_CONST, READ, SGN, WRITE, Instruction

SPEC_PROGRAM = [
    Instruction(LOAD_CONST, 847),
    Instruction(READ, 846),
    Instruction(WRITE, 697),
    Instruction(SGN),
]
SPEC_CODE = bytes.fromhex("FE690000DD69003C570003")


class DecoderTest(unittest.TestCase):
    """Проверки разбора байтов на команды."""

    def test_spec_program(self):
        """Байты из спецификации дают команды из спецификации."""
        self.assertEqual(decode_program(SPEC_CODE), SPEC_PROGRAM)

    def test_round_trip(self):
        """Кодирование и разбор взаимно обратны."""
        program = [Instruction(LOAD_CONST, 2**26 - 1), Instruction(SGN)]
        self.assertEqual(decode_program(encode_program(program)), program)

    def test_decode_at_address(self):
        """Команда читается с заданного адреса памяти команд."""
        instruction = decode_instruction(SPEC_CODE, 4)
        self.assertEqual(str(instruction), "A=29, B=846")

    def test_unknown_opcode(self):
        """Неизвестный код операции даёт ошибку."""
        with self.assertRaisesRegex(InterpreterError, "A=31"):
            decode_instruction(bytes([31]), 0)

    def test_truncated(self):
        """Команда, обрезанная концом программы, даёт ошибку."""
        with self.assertRaisesRegex(InterpreterError, "обрезана"):
            decode_program(SPEC_CODE[:2])

    def test_unused_bits(self):
        """Занятые старшие биты за полем B дают ошибку."""
        with self.assertRaisesRegex(InterpreterError, "старше"):
            decode_instruction(bytes([0x23]), 0)


if __name__ == "__main__":
    unittest.main()
