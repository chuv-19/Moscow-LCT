@echo off
REM Two-Stage Detection Web Interface for Windows

echo ====================================
echo    Two-Stage Detection
echo    (Trees + Defects)
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
echo Starting two-stage detection interface...
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

streamlit run two_stage_web.py

pause
