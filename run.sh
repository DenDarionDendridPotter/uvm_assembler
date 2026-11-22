#!/bin/sh
# Запуск ассемблера УВМ. Аргументы передаются программе.
cd "$(dirname "$0")" || exit 1
python3 -m src.main "$@"
