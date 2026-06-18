#!/bin/bash

# ==============================================================================
# Tree Detection System - Complete Setup Script
# ==============================================================================
# This script installs everything needed to run the tree detection system
# from scratch. Just run this and you're ready to go!
# ==============================================================================

set -e  # Exit on any error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Functions
print_header() {
    echo ""
    echo "=============================================================="
    echo "$1"
    echo "=============================================================="
    echo ""
}

print_success() {
    echo -e "${GREEN}✅ $1${NC}"
}

print_error() {
    echo -e "${RED}❌ $1${NC}"
}

print_info() {
    echo -e "${BLUE}ℹ️  $1${NC}"
}

print_warning() {
    echo -e "${YELLOW}⚠️  $1${NC}"
}

# ==============================================================================
# Step 1: Check System Requirements
# ==============================================================================

print_header "Step 1: Checking System Requirements"

# Check if Python is installed
if command -v python3 &> /dev/null; then
    PYTHON_VERSION=$(python3 --version | cut -d' ' -f2)
    print_success "Python found: $PYTHON_VERSION"
else
    print_error "Python 3 is not installed!"
    print_info "Please install Python 3.8+ from https://www.python.org/"
    exit 1
fi

# Check Python version (need 3.8+)
PYTHON_MAJOR=$(python3 -c 'import sys; print(sys.version_info.major)')
PYTHON_MINOR=$(python3 -c 'import sys; print(sys.version_info.minor)')

if [ "$PYTHON_MAJOR" -lt 3 ] || ([ "$PYTHON_MAJOR" -eq 3 ] && [ "$PYTHON_MINOR" -lt 8 ]); then
    print_error "Python 3.8+ required. You have Python $PYTHON_MAJOR.$PYTHON_MINOR"
    exit 1
fi

print_success "Python version is compatible"

# Check if pip is installed
if command -v pip3 &> /dev/null; then
    print_success "pip3 found"
else
    print_error "pip3 is not installed!"
    print_info "Installing pip..."
    python3 -m ensurepip --upgrade
fi

# Check available disk space (need ~2GB)
if [[ "$OSTYPE" == "darwin"* ]]; then
    FREE_SPACE=$(df -g . | awk 'NR==2 {print $4}')
    print_info "Available disk space: ${FREE_SPACE}GB"
    if [ "$FREE_SPACE" -lt 2 ]; then
        print_warning "Low disk space. Recommended: 2GB+. You have: ${FREE_SPACE}GB"
    fi
fi

# ==============================================================================
# Step 2: Create Virtual Environment (Optional but Recommended)
# ==============================================================================

print_header "Step 2: Python Environment Setup"

read -p "Do you want to create a virtual environment? (Recommended) [Y/n]: " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]] || [[ -z $REPLY ]]; then
    if [ -d "venv" ]; then
        print_warning "Virtual environment already exists. Skipping creation."
    else
        print_info "Creating virtual environment..."
        python3 -m venv venv
        print_success "Virtual environment created"
    fi
    
    print_info "Activating virtual environment..."
    source venv/bin/activate
    print_success "Virtual environment activated"
    
    # Upgrade pip in venv
    pip install --upgrade pip
else
    print_info "Skipping virtual environment creation"
fi

# ==============================================================================
# Step 3: Install Dependencies
# ==============================================================================

print_header "Step 3: Installing Dependencies"

print_info "This will install:"
echo "  - PyTorch (deep learning framework)"
echo "  - Ultralytics YOLOv11 (object detection)"
echo "  - Streamlit (web interface)"
echo "  - OpenCV (image processing)"
echo "  - And other required packages"
echo ""

read -p "Continue with installation? [Y/n]: " -n 1 -r
echo
if [[ ! $REPLY =~ ^[Nn]$ ]]; then
    
    # Create requirements.txt if it doesn't exist
    if [ ! -f "requirements.txt" ]; then
        print_info "Creating requirements.txt..."
        cat > requirements.txt << 'EOF'
# Deep Learning
torch>=2.0.0
torchvision>=0.15.0

# YOLO
ultralytics>=8.0.0

# Web Interface
streamlit>=1.28.0

# Image Processing
opencv-python>=4.8.0
opencv-python-headless>=4.8.0
Pillow>=10.0.0

# Data Processing
numpy>=1.24.0
pandas>=2.0.0

# Other
pyyaml>=6.0
tqdm>=4.65.0
matplotlib>=3.7.0
EOF
        print_success "requirements.txt created"
    fi
    
    print_info "Installing packages (this may take 5-10 minutes)..."
    pip install -r requirements.txt
    
    print_success "All dependencies installed!"
else
    print_warning "Skipping dependency installation"
fi

# ==============================================================================
# Step 4: Verify Installation
# ==============================================================================

print_header "Step 4: Verifying Installation"

# Test imports
print_info "Testing package imports..."

python3 << 'PYEND'
import sys

packages = {
    'torch': 'PyTorch',
    'torchvision': 'TorchVision',
    'ultralytics': 'Ultralytics YOLO',
    'streamlit': 'Streamlit',
    'cv2': 'OpenCV',
    'PIL': 'Pillow',
    'numpy': 'NumPy',
    'pandas': 'Pandas'
}

failed = []
for module, name in packages.items():
    try:
        __import__(module)
        print(f"✅ {name}")
    except ImportError:
        print(f"❌ {name} - FAILED")
        failed.append(name)

if failed:
    print(f"\n⚠️  Failed to import: {', '.join(failed)}")
    sys.exit(1)
else:
    print("\n✅ All packages verified!")
PYEND

if [ $? -eq 0 ]; then
    print_success "All packages working correctly!"
else
    print_error "Some packages failed to import. Please check the error messages above."
    exit 1
fi

# ==============================================================================
# Step 5: Check Models
# ==============================================================================

print_header "Step 5: Checking Models"

TREE_MODEL="runs/detect/tree_detection_cpu/weights/best.pt"
DEFECT_MODEL="runs/defects/tree_defects_detection2/weights/best.pt"

if [ -f "$TREE_MODEL" ]; then
    SIZE=$(du -h "$TREE_MODEL" | cut -f1)
    print_success "Tree detection model found ($SIZE)"
else
    print_error "Tree detection model not found at: $TREE_MODEL"
    print_info "You need to train the model first with: ./train_trees.bat"
fi

if [ -f "$DEFECT_MODEL" ]; then
    SIZE=$(du -h "$DEFECT_MODEL" | cut -f1)
    print_success "Defect detection model found ($SIZE)"
else
    print_error "Defect detection model not found at: $DEFECT_MODEL"
    print_info "You need to train the model first with: ./train_defects.bat"
fi

# ==============================================================================
# Step 6: Make Scripts Executable
# ==============================================================================

print_header "Step 6: Setting Up Launch Scripts"

# Find all .sh files and make them executable
if ls *.sh 1> /dev/null 2>&1; then
    chmod +x *.sh
    print_success "Made all .sh files executable"
fi

# List available launchers
print_info "Available launch scripts:"
echo ""
echo "  ./start_app.sh              - Start main web app (localhost)"
echo "  ./start_app_network.sh      - Start with network access (for phones)"
echo "  ./start_mobile_app.sh       - Start mobile-optimized PWA"
echo "  ./start_desktop_app.sh      - Start desktop GUI (Windows/Linux)"
echo "  ./start_two_stage.sh        - Start two-stage detection web app"
echo ""

# ==============================================================================
# Step 7: Configuration Check
# ==============================================================================

print_header "Step 7: Checking Configuration"

if [ -f "config.ini" ]; then
    print_success "config.ini found"
    
    # Show current configuration
    print_info "Current configuration:"
    grep -E "project_root|tree_model_path|defect_model_path" config.ini | sed 's/^/  /'
else
    print_warning "config.ini not found"
    print_info "The app will use default configuration"
fi

# ==============================================================================
# Step 8: Test Run
# ==============================================================================

print_header "Step 8: Test Run (Optional)"

read -p "Do you want to test the installation by starting the app? [Y/n]: " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]] || [[ -z $REPLY ]]; then
    print_info "Starting the web app..."
    print_info "The app will open in your browser at http://localhost:8501"
    print_info "Press Ctrl+C to stop the server when done testing"
    echo ""
    sleep 2
    
    streamlit run app_mobile.py --server.port=8501 --server.headless=false
else
    print_info "Skipping test run"
fi

# ==============================================================================
# Installation Complete!
# ==============================================================================

print_header "✅ Installation Complete!"

echo ""
print_success "Everything is set up and ready to use!"
echo ""
print_info "Quick Start Guide:"
echo ""
echo "  1. Start the app:"
echo "     ${GREEN}./start_mobile_app.sh${NC}"
echo ""
echo "  2. Access from computer:"
echo "     ${BLUE}http://localhost:8501${NC}"
echo ""
echo "  3. Access from phone:"
echo "     a) Start with: ${GREEN}./start_app_network.sh${NC}"
echo "     b) Find your IP: ${BLUE}ifconfig | grep 'inet '${NC}"
echo "     c) Open on phone: ${BLUE}http://YOUR_IP:8501${NC}"
echo "     d) Tap 'Install app' in browser menu"
echo ""
print_info "Documentation:"
echo "  - README files: ls *README*.md"
echo "  - Configuration: CONFIG_GUIDE.md"
echo "  - Architecture: ARCHITECTURE.md"
echo ""

if [ -d "venv" ]; then
    print_warning "Note: Remember to activate virtual environment before running:"
    echo "  ${YELLOW}source venv/bin/activate${NC}"
    echo ""
fi

print_success "Happy tree detecting! 🌲"
echo ""
