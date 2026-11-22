"""Тесты модели памяти и выполнения команд УВМ."""

import unittest

from src.encoder import encode_program
from src.errors import InterpreterError
from src.isa import LOAD_CONST, READ, SGN, WRITE, Instruction
from src.machine import DATA_SIZE, Machine
from src.parser import load_program
from tests.test_parser import PROGRAMS

COPY_SOURCE = 10
COPY_TARGET = 20
COPY_VALUES = [5, 17, 0, 1, 42, 1000, 65535, 67108863]


def make_machine(*instructions):
    """Создать машину с программой из перечисленных команд.

    :param instructions: команды Instruction.
    :returns: машина Machine с загруженной программой.
    """
    return Machine(encode_program(instructions))


class MachineTest(unittest.TestCase):
    """Проверки команд загрузки, чтения и записи."""

    def test_memory_is_separate(self):
        """Запись в память данных не меняет память команд."""
        machine = make_machine(
            Instruction(LOAD_CONST, 7), Instruction(WRITE, 0)
        )
        code = machine.code
        machine.run()
        self.assertEqual(len(machine.data), DATA_SIZE)
        self.assertEqual(machine.data[0], 7)
        self.assertEqual(machine.code, code)
        self.assertEqual(code[:4], bytes.fromhex("FE000000"))

    def test_load_const(self):
        """Загрузка константы помещает поле B в аккумулятор."""
        machine = make_machine(Instruction(LOAD_CONST, 847))
        machine.run()
        self.assertEqual(machine.acc, 847)

    def test_write(self):
        """Запись помещает аккумулятор в ячейку с адресом B."""
        machine = make_machine(
            Instruction(LOAD_CONST, 99), Instruction(WRITE, 697)
        )
        machine.run()
        self.assertEqual(machine.data[697], 99)

    def test_read_uses_acc_plus_offset(self):
        """Чтение берёт ячейку с адресом аккумулятор + B."""
        machine = make_machine(
            Instruction(LOAD_CONST, 55),
            Instruction(WRITE, 105),
            Instruction(LOAD_CONST, 100),
            Instruction(READ, 5),
        )
        self.assertEqual(machine.run(), 4)
        self.assertEqual(machine.acc, 55)

    def test_copy_array_program(self):
        """Тестовая программа копирует массив и не портит исходный."""
        program = load_program(PROGRAMS / "stage3" / "copy_array.json")
        machine = Machine(encode_program(program))
        machine.run()
        size = len(COPY_VALUES)
        source = machine.data[COPY_SOURCE:COPY_SOURCE + size]
        target = machine.data[COPY_TARGET:COPY_TARGET + size]
        self.assertEqual(source, COPY_VALUES)
        self.assertEqual(target, COPY_VALUES)

    def test_read_out_of_memory(self):
        """Чтение за пределами памяти данных даёт ошибку."""
        machine = make_machine(
            Instruction(LOAD_CONST, DATA_SIZE), Instruction(READ, 0)
        )
        with self.assertRaisesRegex(InterpreterError, "вне памяти"):
            machine.run()

    def test_unsupported_command(self):
        """Команда без реализации даёт ошибку с её адресом."""
        machine = make_machine(Instruction(LOAD_CONST, 1), Instruction(SGN))
        with self.assertRaisesRegex(InterpreterError, "адрес команды 4"):
            machine.run()


if __name__ == "__main__":
    unittest.main()
