@echo off
REM Tree Detection Web App with Network Access for Windows

echo ====================================
echo    Tree Detection System
echo    Network Access Enabled
echo ====================================
echo.

REM Activate virtual environment if it exists
if exist "venv\Scripts\activate.bat" (
    echo Activating virtual environment...
    call venv\Scripts\activate.bat
) else if exist ".venv\Scripts\activate.bat" (
    echo Activating virtual environment...
    call .venv\Scripts\activate.bat
) else (
    echo Warning: Virtual environment not found. Using system Python.
)

echo.
echo Starting web application...
echo.
echo Access from:
echo   - This computer: http://localhost:8501
echo   - Your phone: Check the Network URL below
echo.
echo Make sure your phone is on the same WiFi network!
echo.
echo Press Ctrl+C to stop the server
echo ====================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    pause
    exit /b 1
)

REM Launch with network access
streamlit run app.py --server.address=0.0.0.0 --server.port=8501

pause
