@echo off

@REM 若无管理员权限则获取管理员权限
net session 1>NUL 2>NUL && (
goto as_admin
)

%1 mshta vbscript:CreateObject("Shell.Application").ShellExecute("%~s0","","","runas",1)(window.close)&&exit
cd/d "%~dp0"

:as_admin
chcp 65001 >NUL
@title 安装依赖环境

set CURR_PATH=%~dp0
set VENV_PATH=%CURR_PATH%venv
set LOCAL_PYTHON=%VENV_PATH%\Scripts\

if not exist "%VENV_PATH%" (
    echo 创建虚拟环境
    python -m venv "%VENV_PATH%"
)

if %ERRORLEVEL% NEQ 0 (
    echo 创建虚拟环境返回异常: %ERRORLEVEL%
    goto end
)

echo 开始安装依赖
"%LOCAL_PYTHON%\pip.exe" install -r "%CURR_PATH%\requirements.txt" -i https://pypi.doubanio.com/simple/
if %ERRORLEVEL% NEQ 0 (
    echo 安装返回异常: %ERRORLEVEL%
) else (
    echo 安装完成，按任意键退出
)

:end
pause >NUL
