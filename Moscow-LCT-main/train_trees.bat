@echo off
REM Train Tree Detection Model for Windows

echo ====================================
echo    Train Tree Detection Model
echo ====================================
echo.
echo This will train the tree detection model
echo Training may take a while depending on your hardware
echo.
echo Press Ctrl+C to cancel, or
pause
echo.
echo Starting training...
echo ====================================
echo.

python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed
    pause
    exit /b 1
)

REM Check if ultralytics is installed
python -c "import ultralytics" >nul 2>&1
if errorlevel 1 (
    echo ERROR: Ultralytics YOLO is not installed
    echo Installing required packages...
    pip install ultralytics
)

python train_cpu.py

echo.
echo ====================================
echo Training complete!
echo ====================================
pause
