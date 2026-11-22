"""Перевод промежуточного представления в машинный код УВМ.

Поле A занимает младшие биты команды, поле B сдвигается на номер своего
младшего бита. Получившееся число записывается в size байт от младшего
к старшему (little-endian).
"""

BYTE_ORDER = "little"


def encode_instruction(instruction):
    """Перевести одну команду в машинный код.

    :param instruction: команда Instruction.
    :returns: байты команды, их число равно размеру команды.
    """
    spec = instruction.spec
    word = spec.opcode
    if spec.operand is not None:
        word |= instruction.operand << spec.low_bit
    return word.to_bytes(spec.size, BYTE_ORDER)


def encode_program(program):
    """Перевести программу в машинный код.

    :param program: список команд Instruction.
    :returns: байты всей программы подряд.
    """
    return b"".join(encode_instruction(item) for item in program)


def format_bytes(data):
    """Записать байты так, как в тестах спецификации: 0xFE, 0x69.

    :param data: байты.
    :returns: строка с шестнадцатеричными значениями через запятую.
    """
    return ", ".join(f"0x{byte:02X}" for byte in data)
