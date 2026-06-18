#!/bin/bash
# Quick test script to verify packaging readiness

echo "🔍 Testing Application Portability & Packaging Readiness"
echo "=========================================================="
echo ""

# Test 1: Check Python environment
echo "1️⃣ Checking Python environment..."
python3 --version
if [ $? -eq 0 ]; then
    echo "   ✅ Python found"
else
    echo "   ❌ Python not found"
    exit 1
fi

# Test 2: Check virtual environment
echo ""
echo "2️⃣ Checking virtual environment..."
which python3 | grep -q ".venv"
if [ $? -eq 0 ]; then
    echo "   ✅ Virtual environment active"
else
    echo "   ⚠️  Virtual environment not active (but OK if packages installed)"
fi

# Test 3: Check key dependencies
echo ""
echo "3️⃣ Checking key dependencies..."
python3 -c "import torch; print(f'   ✅ PyTorch {torch.__version__}')" 2>&1 | grep "✅"
python3 -c "import ultralytics; print(f'   ✅ Ultralytics {ultralytics.__version__}')" 2>&1 | grep "✅"
python3 -c "import streamlit; print(f'   ✅ Streamlit {streamlit.__version__}')" 2>&1 | grep "✅"
python3 -c "import cv2; print(f'   ✅ OpenCV {cv2.__version__}')" 2>&1 | grep "✅"
python3 -c "import PyInstaller; print(f'   ✅ PyInstaller {PyInstaller.__version__}')" 2>&1 | grep "✅"

# Test 4: Check for hardcoded paths
echo ""
echo "4️⃣ Checking for hardcoded paths..."
if grep -r "/Users/hanqnero" *.py *.ini 2>/dev/null | grep -v "args.yaml" | grep -q "."; then
    echo "   ⚠️  Hardcoded paths found (check output above)"
else
    echo "   ✅ No hardcoded paths in Python/config files"
fi

# Test 5: Check model files
echo ""
echo "5️⃣ Checking trained models..."
if [ -f "runs/detect/tree_detection_cpu/weights/best.pt" ]; then
    echo "   ✅ Tree detection model found"
else
    echo "   ❌ Tree detection model missing"
fi

if [ -f "runs/defects/tree_defects_detection2/weights/best.pt" ]; then
    echo "   ✅ Defect detection model found"
else
    echo "   ⚠️  Defect detection model missing (optional)"
fi

# Test 6: Check build script
echo ""
echo "6️⃣ Checking build script..."
if [ -f "build_exe.sh" ]; then
    echo "   ✅ build_exe.sh exists"
    if [ -x "build_exe.sh" ]; then
        echo "   ✅ build_exe.sh is executable"
    else
        echo "   ⚠️  build_exe.sh is not executable (run: chmod +x build_exe.sh)"
    fi
else
    echo "   ❌ build_exe.sh not found"
fi

# Test 7: Project size
echo ""
echo "7️⃣ Checking project size..."
echo "   📊 Total project size: $(du -sh . | cut -f1)"
echo "   📊 Virtual env size: $(du -sh .venv 2>/dev/null | cut -f1 || echo 'N/A')"
echo "   📊 Models size: $(du -sh runs 2>/dev/null | cut -f1 || echo 'N/A')"

# Summary
echo ""
echo "=========================================================="
echo "✨ Portability Test Complete!"
echo ""
echo "Next Steps:"
echo "  • To build executable: ./build_exe.sh"
echo "  • To package source: tar -czf TreeDetection.tar.gz *.py runs/ config.ini requirements.txt"
echo "  • To deploy cloud: Push to GitHub and connect to Streamlit Cloud"
echo ""
echo "See PORTABILITY_PACKAGING_REPORT.md for detailed analysis"
echo "=========================================================="
