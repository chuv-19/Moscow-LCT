@echo off
REM Build standalone executable for Tree Detection System
REM This creates a single .exe file that can run without Python installed

echo.
echo ==================================
echo Building Standalone Executable
echo ==================================
echo.

REM Check Python
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] Python not found. Please install Python first.
    pause
    exit /b 1
)

for /f "tokens=2" %%i in ('python --version') do echo [OK] Python found: %%i
echo.

REM Install PyInstaller
echo Installing PyInstaller...
pip install pyinstaller
echo.

REM Run build script
echo Building executable...
python build_exe.py

echo.
echo Done! Check the 'dist' folder for your .exe file.
pause
