@echo off
setlocal

if not exist .venv\Scripts\python.exe (
  echo Run setup_windows.bat first.
  pause
  exit /b 1
)

set /p MAX_PRODUCTS=How many ranking products should be checked? (example 20): 
if "%MAX_PRODUCTS%"=="" set MAX_PRODUCTS=20

call .venv\Scripts\activate.bat
python main.py --max-products %MAX_PRODUCTS%

echo.
pause
