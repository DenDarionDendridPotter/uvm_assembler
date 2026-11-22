@echo off
cd /d "%~dp0\.."
chcp 65001 >nul
REM Этап 3: копирование массива интерпретатором, дамп памяти и ошибки.

echo === ассемблирование programs\stage3\copy_array.json
call .\run.bat asm programs\stage3\copy_array.json out\copy_array.bin
echo.
echo === выполнение, дамп ячеек 10..27 (исходный массив 10..17, копия 20..27)
call .\run.bat vm out\copy_array.bin out\copy_array.csv 10:27
echo.
echo === содержимое out\copy_array.csv:
type out\copy_array.csv
echo.
echo === ошибка выполнения: чтение за пределами памяти данных
call .\run.bat asm programs\stage3\bad_read_address.json out\bad_read_address.bin
call .\run.bat vm out\bad_read_address.bin out\bad_read_address.csv 0:9
echo.
echo === ошибка диапазона адресов
call .\run.bat vm out\copy_array.bin out\copy_array.csv 27:10
echo.
echo === файл программы не найден
call .\run.bat vm out\no_such_program.bin out\copy_array.csv 0:9
