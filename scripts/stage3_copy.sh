#!/bin/sh
# Этап 3: копирование массива интерпретатором, дамп памяти и ошибки.
cd "$(dirname "$0")/.." || exit 1

echo "=== ассемблирование programs/stage3/copy_array.json"
./run.sh asm programs/stage3/copy_array.json out/copy_array.bin
echo
echo "=== выполнение, дамп ячеек 10..27 (исходный массив 10..17, копия 20..27)"
./run.sh vm out/copy_array.bin out/copy_array.csv 10:27
echo
echo "=== содержимое out/copy_array.csv:"
cat out/copy_array.csv
echo
echo "=== ошибка выполнения: чтение за пределами памяти данных"
./run.sh asm programs/stage3/bad_read_address.json out/bad_read_address.bin
./run.sh vm out/bad_read_address.bin out/bad_read_address.csv 0:9
echo
echo "=== ошибка диапазона адресов"
./run.sh vm out/copy_array.bin out/copy_array.csv 27:10
echo
echo "=== файл программы не найден"
./run.sh vm out/no_such_program.bin out/copy_array.csv 0:9
