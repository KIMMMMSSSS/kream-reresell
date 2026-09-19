@echo off
setlocal

if not exist .venv\Scripts\python.exe (
  echo Run setup_windows.bat first.
  pause
  exit /b 1
)

set /p PRODUCT_ID=KREAM product ID: 
set /p SIZE=Size (example 240): 
set /p BID_PRICE=Test bid price in won (example 131000): 

call .venv\Scripts\activate.bat
python main.py --product-id %PRODUCT_ID% --size %SIZE% --bid-price %BID_PRICE%

echo.
pause
