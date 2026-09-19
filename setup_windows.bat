@echo off
setlocal

where py >nul 2>nul
if errorlevel 1 (
  echo [ERROR] Python launcher ^(py^) not found.
  echo Install Python 3.12 from python.org, then run this file again.
  pause
  exit /b 1
)

if not exist .venv (
  py -m venv .venv
  if errorlevel 1 goto :fail
)

call .venv\Scripts\activate.bat
python -m pip install --upgrade pip
pip install -r requirements.txt
python -m playwright install chromium

echo.
echo Setup complete.
pause
exit /b 0

:fail
echo.
echo Setup failed.
pause
exit /b 1
