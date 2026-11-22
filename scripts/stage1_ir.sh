#!/bin/sh
# Этап 1: промежуточное представление тестов спецификации и ошибки разбора.
cd "$(dirname "$0")/.." || exit 1

echo "=== тесты из спецификации УВМ, ожидается:"
echo "A=30, B=847"
echo "A=29, B=846"
echo "A=28, B=697"
echo "A=3"
echo
echo "=== программа programs/spec_tests.json, режим тестирования:"
./run.sh asm programs/spec_tests.json out/spec_tests.bin --test
for file in programs/errors/*.json; do
    echo
    echo "=== $file"
    ./run.sh asm "$file" out/error.bin
done
