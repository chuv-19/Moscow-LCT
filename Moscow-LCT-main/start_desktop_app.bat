@echo off
REM Tree Detection Desktop Application Launcher for Windows

echo ====================================
echo    Tree Detection Desktop App
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
echo Starting desktop application...
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python 3.8+ from https://www.python.org/
    pause
    exit /b 1
)

REM Check if required packages are installed
python -c "import tkinter" >nul 2>&1
if errorlevel 1 (
    echo ERROR: Tkinter is not installed
    echo Tkinter should come with Python. Please reinstall Python.
    pause
    exit /b 1
)

python -c "import PIL" >nul 2>&1
if errorlevel 1 (
    echo Installing Pillow...
    pip install Pillow
)

python -c "import cv2" >nul 2>&1
if errorlevel 1 (
    echo Installing OpenCV...
    pip install opencv-python
)

python -c "import ultralytics" >nul 2>&1
if errorlevel 1 (
    echo Installing Ultralytics...
    pip install ultralytics
)

echo.
echo Launching application...
echo.

REM Launch the GUI application
python app_gui.py

REM Keep window open if there's an error
if errorlevel 1 (
    echo.
    echo An error occurred.
    pause
)
