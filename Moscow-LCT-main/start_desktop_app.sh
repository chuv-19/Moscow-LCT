#!/bin/bash
# Tree Detection Desktop Application Launcher

echo "===================================="
echo "   Tree Detection Desktop App"
echo "===================================="
echo ""

# Activate virtual environment if it exists
if [ -d "venv" ]; then
    echo "Activating virtual environment..."
    source venv/bin/activate
elif [ -d ".venv" ]; then
    echo "Activating virtual environment..."
    source .venv/bin/activate
else
    echo "⚠️  Virtual environment not found. Using system Python."
fi

echo ""
echo "Starting desktop application..."
echo ""

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "ERROR: Python 3 is not installed"
    echo "Please install Python 3.8+ from https://www.python.org/"
    exit 1
fi

# Check and install required packages
python3 -c "import tkinter" 2>/dev/null
if [ $? -ne 0 ]; then
    echo "ERROR: Tkinter is not installed"
    echo "Install with: sudo apt-get install python3-tk (Ubuntu/Debian)"
    echo "Or: brew install python-tk (macOS)"
    exit 1
fi

python3 -c "import PIL" 2>/dev/null
if [ $? -ne 0 ]; then
    echo "Installing Pillow..."
    pip3 install Pillow
fi

python3 -c "import cv2" 2>/dev/null
if [ $? -ne 0 ]; then
    echo "Installing OpenCV..."
    pip3 install opencv-python
fi

python3 -c "import ultralytics" 2>/dev/null
if [ $? -ne 0 ]; then
    echo "Installing Ultralytics..."
    pip3 install ultralytics
fi

echo ""
echo "Launching application..."
echo ""

# Launch the GUI application
python3 app_gui.py
