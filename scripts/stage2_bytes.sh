#!/bin/sh
# Этап 2: машинный код тестов спецификации и запись двоичного файла.
cd "$(dirname "$0")/.." || exit 1

echo "=== тесты из спецификации УВМ, ожидается:"
echo "0xFE, 0x69, 0x00, 0x00"
echo "0xDD, 0x69, 0x00"
echo "0x3C, 0x57, 0x00"
echo "0x03"
echo
echo "=== программа programs/spec_tests.json, режим тестирования:"
./run.sh asm programs/spec_tests.json out/spec_tests.bin --test
echo
echo "=== содержимое файла out/spec_tests.bin:"
python3 -c "print(open('out/spec_tests.bin', 'rb').read().hex(' ').upper())"
echo
echo "=== без режима тестирования:"
./run.sh asm programs/spec_tests.json out/spec_tests.bin
