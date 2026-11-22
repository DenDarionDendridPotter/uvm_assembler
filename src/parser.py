"""Разбор программы на языке ассемблера (JSON) в промежуточное
представление.

Программа это JSON-массив объектов, по одному на команду:

    [
      {"op": "load_const", "constant": 847},
      {"op": "read", "offset": 846},
      {"op": "write", "address": 697},
      {"op": "sgn", "comment": "знак аккумулятора"}
    ]
"""

import json
from pathlib import Path

from .errors import AssemblerError
from .isa import BY_NAME, Instruction

OP_KEY = "op"
COMMENT_KEY = "comment"
KNOWN_NAMES = ", ".join(BY_NAME)


def load_program(path):
    """Прочитать файл с программой и перевести её в промежуточное
    представление.

    :param path: путь к файлу на языке ассемблера.
    :returns: список команд Instruction.
    :raises AssemblerError: если файл не прочитан или программа неверна.
    """
    try:
        text = Path(path).read_text(encoding="utf-8")
    except FileNotFoundError:
        raise AssemblerError(f"файл программы не найден: {path}") from None
    except (OSError, UnicodeDecodeError) as error:
        raise AssemblerError(f"не удалось прочитать {path}: {error}") from None
    return parse_program(text)


def parse_program(text):
    """Перевести текст программы в промежуточное представление.

    :param text: текст программы в формате JSON.
    :returns: список команд Instruction.
    :raises AssemblerError: если JSON испорчен или команда неверна.
    """
    try:
        data = json.loads(text)
    except json.JSONDecodeError as error:
        raise AssemblerError(
            f"неверный JSON (строка {error.lineno}, столбец {error.colno}): "
            f"{error.msg}"
        ) from None
    if not isinstance(data, list):
        raise AssemblerError("программа должна быть JSON-массивом команд")
    if not data:
        raise AssemblerError("программа не содержит ни одной команды")
    return [parse_command(item, number) for number, item in enumerate(data, 1)]


def parse_command(item, number):
    """Перевести одну команду в промежуточное представление.

    :param item: объект JSON с описанием команды.
    :param number: номер команды в программе, начиная с 1.
    :returns: команда Instruction.
    :raises AssemblerError: если команда неверна; в тексте есть номер.
    """
    if not isinstance(item, dict):
        raise AssemblerError(f"команда {number}: ожидается объект JSON")
    name = item.get(OP_KEY)
    if name is None:
        raise AssemblerError(f"команда {number}: не указано поле \"{OP_KEY}\"")
    spec = BY_NAME.get(name)
    if spec is None:
        raise AssemblerError(
            f"команда {number}: неизвестная команда {name!r}, "
            f"допустимы: {KNOWN_NAMES}"
        )
    _check_keys(item, spec, number)
    if spec.operand is None:
        return Instruction(spec)
    return Instruction(spec, _operand(item, spec, number))


def _check_keys(item, spec, number):
    """Проверить, что у команды нет лишних полей.

    :param item: объект JSON с описанием команды.
    :param spec: описание команды из спецификации.
    :param number: номер команды в программе.
    :raises AssemblerError: если встретилось лишнее поле или комментарий
        не строка.
    """
    allowed = {OP_KEY, COMMENT_KEY, spec.operand}
    extra = sorted(key for key in item if key not in allowed)
    if extra:
        raise AssemblerError(
            f"команда {number} ({spec.name}): лишние поля: {', '.join(extra)}"
        )
    comment = item.get(COMMENT_KEY, "")
    if not isinstance(comment, str):
        raise AssemblerError(
            f"команда {number}: поле \"{COMMENT_KEY}\" должно быть строкой"
        )


def _operand(item, spec, number):
    """Получить значение операнда и проверить его диапазон.

    :param item: объект JSON с описанием команды.
    :param spec: описание команды из спецификации.
    :param number: номер команды в программе.
    :returns: значение поля B.
    :raises AssemblerError: если операнда нет, он не целое число или не
        помещается в поле B.
    """
    prefix = f"команда {number} ({spec.name})"
    if spec.operand not in item:
        raise AssemblerError(f"{prefix}: не указано поле \"{spec.operand}\"")
    value = item[spec.operand]
    if isinstance(value, bool) or not isinstance(value, int):
        raise AssemblerError(
            f"{prefix}: поле \"{spec.operand}\" должно быть целым числом, "
            f"получено: {json.dumps(value, ensure_ascii=False)}"
        )
    if not 0 <= value <= spec.max_operand:
        raise AssemblerError(
            f"{prefix}: значение {spec.operand}={value} вне диапазона "
            f"0..{spec.max_operand} (биты {spec.low_bit}-{spec.high_bit})"
        )
    return value
