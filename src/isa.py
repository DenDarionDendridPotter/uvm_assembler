"""Система команд учебной виртуальной машины (вариант 28).

У каждой команды есть поле A (биты 0-4) с кодом операции. У всех
команд, кроме sgn, есть ещё поле B с единственным операндом. Команды
хранятся в памяти в порядке от младшего байта к старшему (little-endian).

| Команда | A | Поле B | Размер |
| --- | --- | --- | --- |
| load_const | 30 | константа, биты 5-30 | 4 байта |
| read | 29 | смещение, биты 5-20 | 3 байта |
| write | 28 | адрес, биты 5-21 | 3 байта |
| sgn | 3 | нет | 1 байт |
"""

from dataclasses import dataclass

OPCODE_BITS = 5
OPCODE_MASK = (1 << OPCODE_BITS) - 1


@dataclass(frozen=True)
class CommandSpec:
    """Описание одной команды УВМ по спецификации.

    :param name: мнемоника команды в языке ассемблера.
    :param opcode: значение поля A.
    :param size: размер команды в байтах.
    :param operand: имя операнда (поля B) в языке ассемблера или None,
        если у команды нет поля B.
    :param low_bit: номер младшего бита поля B.
    :param high_bit: номер старшего бита поля B.
    """

    name: str
    opcode: int
    size: int
    operand: str | None = None
    low_bit: int = OPCODE_BITS
    high_bit: int = OPCODE_BITS - 1

    @property
    def max_operand(self):
        """Наибольшее значение, которое помещается в поле B.

        :returns: 2 в степени ширины поля минус 1 (0, если поля нет).
        """
        width = self.high_bit - self.low_bit + 1
        return (1 << width) - 1


LOAD_CONST = CommandSpec("load_const", 30, 4, "constant", 5, 30)
READ = CommandSpec("read", 29, 3, "offset", 5, 20)
WRITE = CommandSpec("write", 28, 3, "address", 5, 21)
SGN = CommandSpec("sgn", 3, 1)

COMMANDS = (LOAD_CONST, READ, WRITE, SGN)
BY_NAME = {spec.name: spec for spec in COMMANDS}
BY_OPCODE = {spec.opcode: spec for spec in COMMANDS}


@dataclass(frozen=True)
class Instruction:
    """Команда в промежуточном представлении: значения полей A и B.

    :param spec: описание команды из спецификации.
    :param operand: значение поля B или None, если поля нет.
    """

    spec: CommandSpec
    operand: int | None = None

    @property
    def opcode(self):
        """Значение поля A.

        :returns: код операции.
        """
        return self.spec.opcode

    def fields(self):
        """Перечислить поля команды в порядке спецификации.

        :returns: список пар (имя поля, значение).
        """
        pairs = [("A", self.opcode)]
        if self.spec.operand is not None:
            pairs.append(("B", self.operand))
        return pairs

    def __str__(self):
        """Записать поля так, как в тестах спецификации: A=30, B=847.

        :returns: строка с полями и значениями.
        """
        return ", ".join(f"{name}={value}" for name, value in self.fields())
