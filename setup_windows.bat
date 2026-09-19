@echo off
setlocal
cd /d "%~dp0"

echo Working folder: %CD%
echo.

where py >nul 2>nul
if errorlevel 1 (
  echo [ERROR] Python launcher ^(py^) not found.
  echo Install Python 3.12 from python.org and enable "Add Python to PATH".
  echo Then run setup_windows.bat again.
  echo.
  pause
  exit /b 1
)

echo [1/3] Creating Python environment...
if not exist ".venv\Scripts\python.exe" (
  py -m venv .venv
  if errorlevel 1 goto :fail
)

echo [2/3] Installing packages...
call ".venv\Scripts\activate.bat"
python -m pip install --upgrade pip
if errorlevel 1 goto :fail
pip install -r requirements.txt
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

:fail
echo.
echo ========================================
echo SETUP FAILED
echo Take a photo of this window and send it.
echo ========================================
echo.
pause
exit /b 1
