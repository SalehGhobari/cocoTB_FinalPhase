@echo off
cd /d "%~dp0cocoTB_venv\Scripts"
call activate.bat
cd /d "%~dp0testbenches"
start "" "%PROGRAMFILES%\Git\bin\sh.exe" --login
