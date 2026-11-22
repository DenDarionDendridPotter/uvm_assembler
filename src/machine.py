"""Модель УВМ: раздельные память команд и память данных, аккумулятор.

Память команд хранит байты программы и только читается. Память данных
это массив ячеек с целыми числами, все ячейки сначала равны 0. Размер
памяти данных 2**17 ячеек: столько адресов можно записать в поле B
команды записи.
"""

from .decoder import decode_instruction
from .errors import InterpreterError
from .isa import LOAD_CONST, READ, WRITE

DATA_SIZE = WRITE.max_operand + 1


class Machine:
    """Учебная виртуальная машина с регистром-аккумулятором.

    :param code: байты программы, они помещаются в память команд.
    :param data_size: число ячеек памяти данных.
    """

    def __init__(self, code, data_size=DATA_SIZE):
        """Загрузить программу; память данных и аккумулятор равны 0."""
        self.code = bytes(code)
        self.data = [0] * data_size
        self.acc = 0
        self.pc = 0
        self.steps = 0
        self._handlers = {
            LOAD_CONST.name: self._load_const,
            READ.name: self._read,
            WRITE.name: self._write,
        }

    def run(self):
        """Выполнять команды, пока не закончится память команд.

        В системе команд нет переходов, поэтому программа всегда
        завершается.

        :returns: число выполненных команд.
        :raises InterpreterError: при ошибке в машинном коде или при
            обращении к адресу вне памяти данных.
        """
        while self.pc < len(self.code):
            self.step()
        return self.steps

    def step(self):
        """Прочитать команду, перевести её в промежуточное представление
        и выполнить.

        :raises InterpreterError: при ошибке команды.
        """
        address = self.pc
        instruction = decode_instruction(self.code, address)
        self.pc += instruction.spec.size
        handler = self._handlers.get(instruction.spec.name)
        if handler is None:
            raise InterpreterError(
                f"адрес команды {address}: команда {instruction.spec.name} "
                "не поддерживается интерпретатором"
            )
        try:
            handler(instruction.operand)
        except InterpreterError as error:
            message = f"адрес команды {address}: {error}"
            raise InterpreterError(message) from None
        self.steps += 1

    def _check_address(self, address):
        """Проверить, что адрес лежит в памяти данных.

        :param address: адрес ячейки.
        :returns: тот же адрес.
        :raises InterpreterError: если адрес вне памяти данных.
        """
        if not 0 <= address < len(self.data):
            raise InterpreterError(
                f"адрес данных {address} вне памяти (0..{len(self.data) - 1})"
            )
        return address

    def _load_const(self, constant):
        """Загрузка константы: аккумулятор = B.

        :param constant: значение поля B.
        """
        self.acc = constant

    def _read(self, offset):
        """Чтение из памяти: аккумулятор = память[аккумулятор + B].

        :param offset: смещение, значение поля B.
        """
        self.acc = self.data[self._check_address(self.acc + offset)]

    def _write(self, address):
        """Запись в память: память[B] = аккумулятор.

        :param address: адрес, значение поля B.
        """
        self.data[self._check_address(address)] = self.acc
