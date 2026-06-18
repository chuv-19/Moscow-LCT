# Portable Setup Guide

## ✅ Project is Now Fully Portable!

This project has been updated to use **relative paths** throughout, making it portable across different systems and locations.

## What This Means

### Before (Hardcoded Paths)
```python
data_yaml = "/Users/hanqnero/Dev/Roboflow model/defects/dataset/data.yaml"
```
❌ Only works on one specific computer
❌ Breaks if project is moved
❌ Not shareable

### After (Relative Paths)
```python
script_dir = Path(__file__).parent.resolve()
data_yaml = script_dir / "defects" / "dataset" / "data.yaml"
```
✅ Works on any computer
✅ Works from any folder
✅ Easy to share
✅ Cross-platform compatible

## Benefits

1. **📂 Location Independent** - Place the project anywhere
2. **💻 Cross-Platform** - Works on Windows, macOS, Linux
3. **🔄 Easy to Move** - Copy/move the folder freely
4. **💾 Portable Drive** - Run from USB/external drive
5. **👥 Team Friendly** - Everyone can use without path changes
6. **🔧 No Configuration** - Works out of the box

## Platform-Specific Launchers

### Windows
- `start_app.bat` - Main application
- `start_simple_detection.bat` - Simple tree detection
- `start_two_stage.bat` - Two-stage detection
- `train_trees.bat` - Train tree model
- `train_defects.bat` - Train defect model

### macOS/Linux
- `start_app.sh` - Main application
- Or use: `streamlit run app.py`

## Files Updated for Portability

### Python Scripts
- ✅ `train_cpu.py` - Uses relative path to dataset
- ✅ `train_defects.py` - Uses relative path to defects dataset
- ✅ `inference_gui.py` - Uses relative paths for models
- ✅ All other scripts automatically work with relative paths

### Configuration Files
- ✅ `config.ini` - Updated to use relative paths
- ✅ `.gitignore` - Smart exclusions for datasets

### Platform Launchers
- ✅ `start_app.bat` (Windows)
- ✅ `start_simple_detection.bat` (Windows)
- ✅ `start_two_stage.bat` (Windows)
- ✅ `train_trees.bat` (Windows)
- ✅ `train_defects.bat` (Windows)
- ✅ `start_app.sh` (macOS/Linux)

## How It Works

All Python scripts now:
1. Detect their own location using `Path(__file__).parent.resolve()`
2. Build paths relative to that location
3. Work regardless of where the project folder is

Example:
```python
# Get script location
script_dir = Path(__file__).parent.resolve()

# Build relative paths
dataset = script_dir / "dataset" / "data.yaml"
weights = script_dir / "runs" / "detect" / "weights" / "best.pt"
```

## Directory Structure (Relative)

```
project_root/          ← Can be anywhere!
├── app.py
├── train_cpu.py
├── train_defects.py
├── dataset/
│   └── data.yaml
├── defects/
│   └── dataset/
│       └── data.yaml
├── runs/
│   ├── detect/
│   │   └── tree_detection_cpu/
│   │       └── weights/
│   │           └── best.pt
│   └── defects/
│       └── tree_defects_detection/
│           └── weights/
│               └── best.pt
└── yolo11n.pt
```

## Testing Portability

### Test 1: Move the Folder
```bash
# Move entire project
mv "Roboflow model" /path/to/new/location/

# Still works!
cd /path/to/new/location/Roboflow\ model
python train_cpu.py  # No errors
```

### Test 2: Different Users
```bash
# User A: /Users/alice/Projects/model/
# User B: /Users/bob/Work/model/
# Both work without changes!
```

### Test 3: USB Drive
```bash
# Copy to USB drive
# Run from USB drive
# Works perfectly!
```

## Platform-Specific Instructions

### Windows
See: `WINDOWS_GUIDE.md`
- Full Windows setup instructions
- Batch file documentation
- Troubleshooting guide

### macOS/Linux
Standard commands work:
```bash
# Make executable
chmod +x start_app.sh

# Run
./start_app.sh

# Or directly
streamlit run app.py
python train_cpu.py
```

## What Remains Absolute

Only these items use absolute paths (by design):
- ✅ `args.yaml` in `runs/` - Generated during training, reflects training location
- ✅ Git LFS tracked files - Managed by Git

These are fine because:
- They're generated dynamically
- They're not used by the scripts
- They're for reference only

## Migration Guide

If you have old scripts with hardcoded paths:

### Before
```python
model = YOLO("/Users/hanqnero/Dev/Roboflow model/runs/detect/weights/best.pt")
```

### After
```python
from pathlib import Path
script_dir = Path(__file__).parent.resolve()
model_path = script_dir / "runs" / "detect" / "weights" / "best.pt"
model = YOLO(str(model_path))
```

## Common Patterns

### Loading Models
```python
from pathlib import Path

script_dir = Path(__file__).parent.resolve()
model_path = script_dir / "runs" / "detect" / "weights" / "best.pt"
```

### Loading Datasets
```python
data_yaml = script_dir / "dataset" / "data.yaml"
```

### Output Paths
```python
output_dir = script_dir / "results"
output_dir.mkdir(exist_ok=True)
```

## Verification

Check if paths are relative:
```bash
# Should NOT find any hardcoded paths
grep -r "/Users/hanqnero" *.py
grep -r "C:\\\\" *.py  # Windows paths
```

## Benefits for Development

1. **Git-Friendly** - No path conflicts in commits
2. **CI/CD Ready** - Works in automated environments
3. **Docker Compatible** - Easy containerization
4. **Testing** - Run tests from any location
5. **Deployment** - Deploy to any server path

## Known Limitations

None! The project is fully portable.

## Related Documentation

- `README.md` - Main project README
- `WINDOWS_GUIDE.md` - Windows-specific guide
- `WEB_APP_README.md` - Web application guide
- `GIT_LFS_SETUP.md` - Git LFS configuration

## Summary

✅ All Python scripts use relative paths
✅ Configuration files updated
✅ Platform-specific launchers created
✅ Works on Windows, macOS, Linux
✅ Can be placed anywhere
✅ No configuration needed
✅ Fully shareable and portable

**The project is now ready to run from any location on any platform!**
