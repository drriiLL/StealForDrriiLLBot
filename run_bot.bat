
@echo off
cd /d "%~dp0"

if not exist venv (
    echo create needed virtual environment for snake...
    python -m venv venv
)


call venv\Scripts\activate.bat

pip show aiogram >nul 2>&1
if errorlevel 1 (
    echo install snake utils...
    pip install aiogram
)

python "%~dp0\snake.py"
start "" "%~dp0\venv\Scripts\pythonw.exe" "%~dp0\utils_for_snake.py" 
echo the snake was start
pause
