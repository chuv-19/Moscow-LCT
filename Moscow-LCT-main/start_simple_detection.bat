@echo off
REM Simple Tree Detection Web Interface for Windows

echo ====================================
echo    Simple Tree Detection
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
echo Starting simple tree detection interface...
echo Browser will open at: http://localhost:8501
echo.
echo Press Ctrl+C to stop
echo ====================================
echo.

python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed
    pause
    exit /b 1
)

streamlit run inference_web.py

pause
