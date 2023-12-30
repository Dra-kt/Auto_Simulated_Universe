@echo off

@REM 若无管理员权限则获取管理员权限
net session 1>NUL 2>NUL && (
goto as_admin
)

%1 mshta vbscript:CreateObject("Shell.Application").ShellExecute("%~s0","","","runas",1)(window.close)&&exit
cd/d "%~dp0"

:as_admin
set CURR_PATH=%~dp0
set VENV_PATH=%CURR_PATH%venv\
set LOCAL_PYTHON=%VENV_PATH%Scripts\

"%LOCAL_PYTHON%python.exe" "%CURR_PATH%states.py" ^
--find=1