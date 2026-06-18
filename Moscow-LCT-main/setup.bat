@echo off
REM ==============================================================================
REM Tree Detection System - Complete Setup Script (Windows)
REM ==============================================================================
REM This script installs everything needed to run the tree detection system
REM from scratch. Just run this and you're ready to go!
REM ==============================================================================

echo.
echo ==============================================================
echo Tree Detection System - Complete Setup
echo ==============================================================
echo.

REM ==============================================================================
REM Step 1: Check Python
REM ==============================================================================

echo Step 1: Checking Python Installation
echo ------------------------------
echo.

python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] Python is not installed!
    echo Please install Python 3.8+ from https://www.python.org/
    echo Make sure to check "Add Python to PATH" during installation
    pause
    exit /b 1
)

for /f "tokens=2" %%i in ('python --version') do set PYTHON_VERSION=%%i
echo [OK] Python found: %PYTHON_VERSION%
echo.

REM ==============================================================================
REM Step 2: Check pip
REM ==============================================================================

echo Step 2: Checking pip
echo ------------------------------
echo.

pip --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] pip is not installed!
    echo Installing pip...
    python -m ensurepip --upgrade
)

echo [OK] pip found
echo.

REM ==============================================================================
REM Step 3: Create Virtual Environment
REM ==============================================================================

echo Step 3: Virtual Environment Setup
echo ------------------------------
echo.

set /p CREATE_VENV="Create virtual environment? (Recommended) [Y/n]: "
if /i "%CREATE_VENV%"=="n" goto skip_venv

if exist "venv\" (
    echo [WARNING] Virtual environment already exists
) else (
    echo Creating virtual environment...
    python -m venv venv
    echo [OK] Virtual environment created
)

echo Activating virtual environment...
call venv\Scripts\activate.bat
echo [OK] Virtual environment activated
echo.

REM Upgrade pip
python -m pip install --upgrade pip

:skip_venv

REM ==============================================================================
REM Step 4: Install Dependencies
REM ==============================================================================

echo.
echo Step 4: Installing Dependencies
echo ------------------------------
echo.
echo This will install:
echo   - PyTorch (deep learning framework)
echo   - Ultralytics YOLOv11 (object detection)
echo   - Streamlit (web interface)
echo   - OpenCV (image processing)
echo   - And other required packages
echo.

set /p INSTALL_DEPS="Continue with installation? [Y/n]: "
if /i "%INSTALL_DEPS%"=="n" goto skip_install

REM Create requirements.txt if not exists
if not exist "requirements.txt" (
    echo Creating requirements.txt...
    (
        echo # Deep Learning
        echo torch^>=2.0.0
        echo torchvision^>=0.15.0
        echo.
        echo # YOLO
        echo ultralytics^>=8.0.0
        echo.
        echo # Web Interface
        echo streamlit^>=1.28.0
        echo.
        echo # Image Processing
        echo opencv-python^>=4.8.0
        echo opencv-python-headless^>=4.8.0
        echo Pillow^>=10.0.0
        echo.
        echo # Data Processing
        echo numpy^>=1.24.0
        echo pandas^>=2.0.0
        echo.
        echo # Other
        echo pyyaml^>=6.0
        echo tqdm^>=4.65.0
        echo matplotlib^>=3.7.0
    ) > requirements.txt
    echo [OK] requirements.txt created
)

echo Installing packages (this may take 5-10 minutes)...
pip install -r requirements.txt

if %errorlevel% neq 0 (
    echo [ERROR] Failed to install dependencies
    pause
    exit /b 1
)

echo [OK] All dependencies installed!

:skip_install

REM ==============================================================================
REM Step 5: Verify Installation
REM ==============================================================================

echo.
echo Step 5: Verifying Installation
echo ------------------------------
echo.

python -c "import torch; print('[OK] PyTorch')" 2>nul || echo [ERROR] PyTorch failed
python -c "import ultralytics; print('[OK] Ultralytics')" 2>nul || echo [ERROR] Ultralytics failed
python -c "import streamlit; print('[OK] Streamlit')" 2>nul || echo [ERROR] Streamlit failed
python -c "import cv2; print('[OK] OpenCV')" 2>nul || echo [ERROR] OpenCV failed
python -c "import PIL; print('[OK] Pillow')" 2>nul || echo [ERROR] Pillow failed
python -c "import numpy; print('[OK] NumPy')" 2>nul || echo [ERROR] NumPy failed

echo.

REM ==============================================================================
REM Step 6: Check Models
REM ==============================================================================

echo Step 6: Checking Models
echo ------------------------------
echo.

if exist "runs\detect\tree_detection_cpu\weights\best.pt" (
    echo [OK] Tree detection model found
) else (
    echo [WARNING] Tree detection model not found
    echo You need to train the model first: train_trees.bat
)

if exist "runs\defects\tree_defects_detection2\weights\best.pt" (
    echo [OK] Defect detection model found
) else (
    echo [WARNING] Defect detection model not found
    echo You need to train the model first: train_defects.bat
)

echo.

REM ==============================================================================
REM Step 7: Configuration
REM ==============================================================================

echo Step 7: Configuration
echo ------------------------------
echo.

if exist "config.ini" (
    echo [OK] config.ini found
) else (
    echo [WARNING] config.ini not found - will use defaults
)

echo.

REM ==============================================================================
REM Installation Complete
REM ==============================================================================

echo.
echo ==============================================================
echo Installation Complete!
echo ==============================================================
echo.
echo Everything is set up and ready to use!
echo.
echo Quick Start:
echo   1. Start the app:
echo      start_mobile_app.bat
echo.
echo   2. Access from computer:
echo      http://localhost:8501
echo.
echo   3. Access from phone:
echo      a) Start with: start_app_network.bat
echo      b) Find your IP: ipconfig
echo      c) Open on phone: http://YOUR_IP:8501
echo      d) Tap 'Install app' in browser menu
echo.
echo Documentation:
echo   - README files: dir *README*.md
echo   - Configuration: CONFIG_GUIDE.md
echo.

if exist "venv\" (
    echo NOTE: Virtual environment created.
    echo Remember to activate it before running:
    echo   venv\Scripts\activate.bat
    echo.
)

echo Happy tree detecting! [tree emoji]
echo.

pause
