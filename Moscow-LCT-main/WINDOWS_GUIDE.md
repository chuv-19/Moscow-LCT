# Windows Quick Start Guide

## Overview
This project is now fully portable and works on Windows! All paths are relative, so you can place the project anywhere on your system.

## Batch File Launchers

We've created easy-to-use batch files for Windows users. Simply double-click to run:

### �️ Desktop Application (NEW!)
**`start_desktop_app.bat`** - Native Windows Desktop App
- **Full GUI application** with Tkinter
- No browser required - runs natively
- Side-by-side image comparison
- Real-time detection with progress bar
- Export annotated images and JSON
- Works completely offline
- **Recommended for Windows users!**

### 🚀 Web Applications
**`start_app.bat`** - Launch the main web interface
- Two-stage detection (trees + defects)
- Browser-based interface
- Automatic dependency checking

**`start_simple_detection.bat`** - Simple tree detection
- Quick tree counting
- Basic tree identification
- Fast processing

**`start_two_stage.bat`** - Two-stage detection (trees + defects)
- Advanced tree detection
- 12 defect types
- Tree health analysis

### 🏋️ Training Scripts

**`train_trees.bat`** - Train tree detection model
- Trains on dataset/data.yaml
- CPU-optimized settings
- ~10 epochs

**`train_defects.bat`** - Train defect detection model
- Trains on defects/dataset/data.yaml
- 40 epochs
- 14 classes (2 trees + 12 defects)

## First Time Setup

### 1. Install Python
Download and install Python 3.8 or newer from:
https://www.python.org/downloads/

**Important:** Check "Add Python to PATH" during installation!

### 2. Install Dependencies
Open Command Prompt in the project folder and run:
```cmd
pip install -r requirements.txt
```

Or simply run `start_app.bat` - it will install dependencies automatically if needed.

### 3. Verify Installation
```cmd
python --version
pip list
```

## Quick Start

### Option 1: Use Batch Files (Easiest)
1. Double-click `start_app.bat`
2. Wait for browser to open
3. Choose your detection type
4. Upload images and analyze

### Option 2: Command Line
Open Command Prompt in project folder:

```cmd
REM Main app
streamlit run app.py

REM Simple detection
streamlit run inference_web.py

REM Two-stage detection
streamlit run two_stage_web.py

REM Training
python train_cpu.py
python train_defects.py
```

## Project Structure

```
Roboflow model/
├── start_app.bat                    ← Main launcher
├── start_simple_detection.bat       ← Simple detection
├── start_two_stage.bat              ← Two-stage detection
├── train_trees.bat                  ← Train tree model
├── train_defects.bat                ← Train defect model
├── app.py                           ← Main web app
├── inference_web.py                 ← Simple detection app
├── two_stage_web.py                 ← Two-stage detection app
├── train_cpu.py                     ← Tree training script
├── train_defects.py                 ← Defect training script
├── dataset/                         ← Tree detection data
├── defects/dataset/                 ← Defect detection data
├── runs/                            ← Training results & weights
│   ├── detect/                      ← Tree models
│   │   └── tree_detection_cpu/
│   │       └── weights/
│   │           └── best.pt          ← Trained tree model
│   └── defects/                     ← Defect models
│       └── tree_defects_detection/
│           └── weights/
│               └── best.pt          ← Trained defect model
└── yolo11n.pt                       ← Base YOLO model
```

## Common Issues & Solutions

### "Python is not recognized"
- Python is not in PATH
- Reinstall Python and check "Add Python to PATH"
- Or add manually: Settings → System → Advanced → Environment Variables

### "Module not found" errors
```cmd
pip install -r requirements.txt
```

### "Port already in use"
Another Streamlit app is running. Either:
- Close the other app
- Use a different port:
  ```cmd
  streamlit run app.py --server.port 8502
  ```

### Model not found
- Train the models first using `train_trees.bat` or `train_defects.bat`
- Or download pre-trained weights from the repository

### Slow training
- Normal on CPU
- Training on GPU is much faster (requires CUDA-capable GPU)
- Consider using Google Colab for free GPU access

## Performance Tips

### For Faster Inference
- Use smaller image sizes (640x640 or less)
- Increase confidence threshold (fewer detections)
- Close other applications

### For Training
- Use GPU if available (10-50x faster)
- Reduce image size in training scripts
- Reduce batch size if running out of memory
- Use fewer epochs for testing

## Using GPU (Optional)

If you have an NVIDIA GPU:

1. Install CUDA Toolkit: https://developer.nvidia.com/cuda-downloads
2. Install PyTorch with CUDA:
   ```cmd
   pip install torch torchvision --index-url https://download.pytorch.org/whl/cu118
   ```
3. Verify GPU is detected:
   ```cmd
   python -c "import torch; print(torch.cuda.is_available())"
   ```

## Portable Installation

This project uses **relative paths**, meaning:
- ✅ No hardcoded paths
- ✅ Works from any folder
- ✅ Can be on USB drive
- ✅ Easy to share/backup
- ✅ Cross-platform compatible

Just copy the entire folder to any location and it will work!

## Getting Help

### Check Logs
When running batch files, any errors will be displayed.
Take a screenshot if you need help.

### Verify Setup
```cmd
python --version
pip list | findstr ultralytics
pip list | findstr streamlit
```

### Test Python Scripts Directly
```cmd
python -c "from ultralytics import YOLO; print('YOLO OK')"
python -c "import streamlit; print('Streamlit OK')"
```

## System Requirements

### Minimum
- Windows 10 or newer
- Python 3.8+
- 4GB RAM
- 2GB free disk space

### Recommended
- Windows 11
- Python 3.10+
- 8GB+ RAM
- NVIDIA GPU with 4GB+ VRAM (optional, for training)

## Next Steps

1. ✅ Run `start_app.bat`
2. ✅ Upload test images
3. ✅ Explore both detection modes
4. ✅ Train custom models if needed
5. ✅ Check training results in `runs/` folder

## Additional Resources

- **Main README**: `README.md`
- **Web App Guide**: `WEB_APP_README.md`
- **Class Information**: `UPDATED_CLASSES_README.md`
- **Git LFS Setup**: `GIT_LFS_SETUP.md`

## Troubleshooting Checklist

- [ ] Python installed and in PATH
- [ ] Dependencies installed (`pip install -r requirements.txt`)
- [ ] No antivirus blocking Python
- [ ] Sufficient disk space (2GB+)
- [ ] No other apps using port 8501
- [ ] Models trained or downloaded

## License

This project is part of the Moscow-LCT repository.
All model weights are tracked with Git LFS.

---

**Need help?** Check the error messages in the Command Prompt window or create an issue on GitHub.
