@echo off
setlocal EnableExtensions
cd /d "%~dp0"

echo ========================================
echo KREAM BOT - FIRST TIME SETUP
echo ========================================
echo Working folder: %CD%
echo.

set "PYTHON_CMD="

call :find_python
if defined PYTHON_CMD goto :python_ready

echo Python 3.12 was not found.
echo Trying to install Python 3.12 automatically with winget...
echo.

where winget >nul 2>nul
if errorlevel 1 (
  echo [ERROR] winget is not available on this PC.
  echo Please install Python 3.12 manually from python.org.
  echo During installation, check "Add Python to PATH".
  echo Then run this file again.
  goto :fail
)

winget install --id Python.Python.3.12 -e --source winget --accept-package-agreements --accept-source-agreements --silent
if errorlevel 1 (
  echo [ERROR] Automatic Python installation failed.
  echo Please install Python 3.12 manually from python.org and run this file again.
  goto :fail
)

echo.
echo Python installation command finished.
echo Detecting the newly installed Python...
call :find_python
if not defined PYTHON_CMD (
  echo [ERROR] Python was installed but this window cannot find it yet.
  echo Close this window and run setup_windows.bat one more time.
  goto :fail
)

:python_ready
echo Using Python: %PYTHON_CMD%
echo.

echo [1/3] Creating Python environment...
if not exist ".venv\Scripts\python.exe" (
  %PYTHON_CMD% -m venv .venv
  if errorlevel 1 goto :fail
)

echo [2/3] Installing packages...
call ".venv\Scripts\activate.bat"
python -m pip install --upgrade pip
if errorlevel 1 goto :fail
python -m pip install -r requirements.txt
if errorlevel 1 goto :fail

echo [3/3] Installing Chromium...
python -m playwright install chromium
if errorlevel 1 goto :fail

echo.
echo ========================================
echo SETUP COMPLETE
echo You can now run run_windows.bat
echo ========================================
echo.
pause
exit /b 0

:find_python
set "PYTHON_CMD="

where py >nul 2>nul
if not errorlevel 1 (
  py -3.12 --version >nul 2>nul
  if not errorlevel 1 (
    set "PYTHON_CMD=py -3.12"
    exit /b 0
  )
)

if exist "%LOCALAPPDATA%\Programs\Python\Python312\python.exe" (
  set PYTHON_CMD="%LOCALAPPDATA%\Programs\Python\Python312\python.exe"
  exit /b 0
)

if exist "%ProgramFiles%\Python312\python.exe" (
  set PYTHON_CMD="%ProgramFiles%\Python312\python.exe"
  exit /b 0
)

where python >nul 2>nul
if not errorlevel 1 (
  python --version >nul 2>nul
  if not errorlevel 1 (
    set "PYTHON_CMD=python"
    exit /b 0
  )
)

exit /b 0

:fail
echo.
echo ========================================
echo SETUP FAILED
echo Take a photo of this window and send it.
echo ========================================
echo.
pause
exit /b 1
