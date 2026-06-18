#!/bin/bash

# Build standalone executable for Tree Detection System
# This creates a single file that can run without Python installed

echo "=================================="
echo "Building Standalone Executable"
echo "=================================="
echo ""

# Check Python
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 not found. Please install Python first."
    exit 1
fi

echo "✅ Python found: $(python3 --version)"
echo ""

# Install PyInstaller if needed
echo "📦 Installing PyInstaller..."
pip install pyinstaller
echo ""

# Run build script
echo "🔨 Building executable..."
python3 build_exe.py

echo ""
echo "Done! Check the 'dist' folder for your executable."
