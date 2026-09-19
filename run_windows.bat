@echo off
setlocal
cd /d "%~dp0"

echo Working folder: %CD%
echo.

if not exist ".venv\Scripts\python.exe" (
  echo [ERROR] Setup has not completed in this folder.
  echo Run setup_windows.bat first and make sure it says SETUP COMPLETE.
  echo.
  pause
  exit /b 1
)

set /p MAX_PRODUCTS=How many ranking products should be checked? (default 100): 
if "%MAX_PRODUCTS%"=="" set MAX_PRODUCTS=100

call ".venv\Scripts\activate.bat"
python main.py --max-products %MAX_PRODUCTS%
set EXIT_CODE=%ERRORLEVEL%

echo.
if not "%EXIT_CODE%"=="0" (
  echo ========================================
  echo PROGRAM ERROR - exit code %EXIT_CODE%
  echo Take a photo of the error above and send it.
  echo ========================================
) else (
  echo Program finished normally.
)
echo.
pause
exit /b %EXIT_CODE%
