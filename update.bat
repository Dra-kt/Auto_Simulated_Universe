@echo off

set CURR_PATH=%~dp0
set VENV_PATH=%CURR_PATH%venv
set LOCAL_PYTHON=%VENV_PATH%Scripts\

"%LOCAL_PYTHON%python.exe" "%CURR_PATH%update.py"
