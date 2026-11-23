@echo off
cd /d "%~dp0\.."
chcp 65001 >nul
REM Этап 1: промежуточное представление тестов спецификации и ошибки разбора.

echo === тесты из спецификации УВМ, ожидается:
echo A=30, B=847
echo A=29, B=846
echo A=28, B=697
echo A=3
echo.
echo === программа programs\spec_tests.json, промежуточное представление (--ir):
call .\run.bat asm programs\spec_tests.json out\spec_tests.bin --ir
for %%F in (programs\errors\*.json) do (
    echo.
    echo === %%F
    call .\run.bat asm %%F out\error.bin
)
