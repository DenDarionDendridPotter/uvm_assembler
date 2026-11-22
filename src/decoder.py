"""Перевод машинного кода УВМ обратно в промежуточное представление.

Код операции берётся из младших 5 бит первого байта команды, по нему
определяется размер команды и положение поля B.
"""

from .encoder import BYTE_ORDER
from .errors import InterpreterError
from .isa import BY_OPCODE, OPCODE_MASK, Instruction


def decode_instruction(code, address):
    """Прочитать одну команду из памяти команд.

    :param code: байты памяти команд.
    :param address: адрес первого байта команды.
    :returns: команда Instruction.
    :raises InterpreterError: если код операции неизвестен, команда
        обрезана концом памяти или в ней заняты неиспользуемые биты.
    """
    opcode = code[address] & OPCODE_MASK
    spec = BY_OPCODE.get(opcode)
    if spec is None:
        raise InterpreterError(
            f"адрес команды {address}: неизвестный код операции A={opcode}"
        )
    end = address + spec.size
    if end > len(code):
        raise InterpreterError(
            f"адрес команды {address}: команда {spec.name} обрезана: "
            f"размер {spec.size} байт, до конца программы "
            f"{len(code) - address}"
        )
    word = int.from_bytes(code[address:end], BYTE_ORDER)
    operand = None
    if spec.operand is not None:
        operand = (word >> spec.low_bit) & spec.max_operand
    if word >> (spec.high_bit + 1):
        raise InterpreterError(
            f"адрес команды {address}: в команде {spec.name} заняты биты "
            f"старше {spec.high_bit}"
        )
    return Instruction(spec, operand)


def decode_program(code):
    """Перевести весь машинный код в промежуточное представление.

    :param code: байты программы.
    :returns: список команд Instruction.
    :raises InterpreterError: если машинный код неверен.
    """
    program = []
    address = 0
    while address < len(code):
        instruction = decode_instruction(code, address)
        program.append(instruction)
        address += instruction.spec.size
    return program
