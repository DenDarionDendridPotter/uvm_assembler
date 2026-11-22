@echo off
REM Запуск ассемблера УВМ. Аргументы передаются программе.
cd /d "%~dp0"
python -m src.main %*
