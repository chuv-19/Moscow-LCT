# Desktop Application Guide

## 🖥️ Tree Detection Desktop Application

A native Windows desktop application built with Tkinter for tree and defect detection. All the power of the web app in a standalone desktop GUI!

## Features

### ✨ Complete Functionality
- 🌲 Two-stage detection (Trees + Defects)
- 📁 Easy image selection with file browser
- 🎚️ Adjustable confidence thresholds (sliders)
- 🖼️ Side-by-side image comparison
- 📊 Detailed results display
- 💾 Export annotated images
- 📄 Save results as JSON
- ⚡ Threaded processing (non-blocking UI)
- 📈 Real-time progress indication

### 🎨 User Interface

#### Left Panel - Controls
- **Model Status**: Shows if models are loaded
- **Image Selection**: Browse and select images
- **Detection Settings**: 
  - Tree confidence slider (0.05 - 0.95)
  - Defect confidence slider (0.05 - 0.95)
- **Run Detection**: Large button to start analysis
- **Export Options**:
  - Save annotated image (JPG/PNG)
  - Save results as JSON
- **Class Information**: List of detectable classes

#### Right Panel - Results
- **Original Image**: Shows uploaded image
- **Detection Results**: Shows annotated image
- **Detection Summary**: Scrollable text with detailed results

#### Status Bar
- Real-time status updates with timestamps

## Installation

### Prerequisites
- Python 3.8 or newer
- Windows 10 or newer (primary), also works on macOS/Linux

### Required Packages
The launcher scripts will auto-install these:
- `tkinter` (included with Python)
- `Pillow` (PIL - image processing)
- `opencv-python` (computer vision)
- `ultralytics` (YOLO models)

## Launching the Application

### Windows

#### Method 1: Batch File (Easiest)
Simply double-click:
```
start_desktop_app.bat
```

The batch file will:
1. Check Python installation
2. Verify/install dependencies
3. Launch the application

#### Method 2: Command Line
```cmd
python app_gui.py
```

### macOS/Linux

#### Method 1: Shell Script
```bash
./start_desktop_app.sh
```

#### Method 2: Direct Command
```bash
python3 app_gui.py
```

## Using the Application

### Step 1: Launch
- Double-click `start_desktop_app.bat` (Windows)
- Wait for window to open

### Step 2: Check Model Status
- Look at "Model Status" panel
- Should show:
  - ✅ Tree Model: Ready
  - ✅ Defect Model: Ready
- If models missing, train them first

### Step 3: Select Image
- Click "📁 Select Image" button
- Browse to your image file
- Supported formats: JPG, JPEG, PNG, BMP
- Image will appear in "Original Image" panel

### Step 4: Adjust Settings (Optional)
- **Tree Confidence**: Higher = fewer but more certain detections
  - Default: 0.25
  - Range: 0.05 - 0.95
- **Defect Confidence**: Lower recommended for better detection
  - Default: 0.20
  - Range: 0.05 - 0.95

### Step 5: Run Detection
- Click "🚀 Run Detection" button
- Progress bar will animate
- Wait for processing to complete
- Results appear in right panel

### Step 6: Review Results
- **Annotated Image**: See detected trees (green boxes) and defects (red boxes)
- **Summary**: View metrics (total trees, defects, healthy/unhealthy)
- **Details**: Scroll through detailed results for each tree

### Step 7: Export (Optional)
- **Save Image**: Click "💾 Save Annotated Image"
  - Choose location and filename
  - Saves as JPG or PNG
  
- **Save JSON**: Click "📄 Save JSON Results"
  - Structured data for further processing
  - Includes all detection information

## Application Layout

```
┌─────────────────────────────────────────────────────────────────┐
│  🌲 Tree & Defect Detection System                              │
│  Two-Stage Detection: Trees + Defects                           │
├──────────────┬──────────────────────────────────────────────────┤
│              │                                                   │
│ Model Status │  Original Image    │  Detection Results         │
│ ✅ Tree OK   │                     │                            │
│ ✅ Defect OK │  [Image Display]    │  [Annotated Image]        │
│              │                     │                            │
│ Image Select │                     │                            │
│ [Browse...]  │                     │                            │
│              │                     │                            │
│ Settings     ├─────────────────────┴────────────────────────────┤
│ Tree: 0.25   │  Detection Summary                               │
│ [====]       │  ┌────────────────────────────────────────────┐ │
│              │  │ Total Trees: 3                             │ │
│ Defect: 0.20 │  │ Total Defects: 5                          │ │
│ [====]       │  │ Healthy: 1                                 │ │
│              │  │ Unhealthy: 2                               │ │
│ [Run Detect] │  │ ────────────────────────────────────────   │ │
│              │  │ ┌─ Tree_1                                  │ │
│ Export       │  │ │  Type: oak                               │ │
│ [Save Image] │  │ │  Defects: crack, rot                     │ │
│ [Save JSON]  │  │ └─                                          │ │
│              │  └────────────────────────────────────────────┘ │
│ Classes      │                                                   │
│ • Bush       │                                                   │
│ • Oak        │                                                   │
│ • Crack      │                                                   │
│ • ...        │                                                   │
└──────────────┴───────────────────────────────────────────────────┤
│ [12:34:56] Ready                                                 │
└──────────────────────────────────────────────────────────────────┘
```

## Advantages Over Web App

| Feature | Desktop App | Web App |
|---------|------------|---------|
| **Offline** | ✅ Fully offline | ⚠️ Requires server |
| **Startup** | ✅ Instant | ⚠️ Start server first |
| **Native Feel** | ✅ Native windows | ⚠️ Browser-based |
| **File Access** | ✅ Direct file browser | ⚠️ Upload only |
| **Performance** | ✅ Direct memory | ⚠️ Temp files |
| **Multitasking** | ✅ Separate window | ⚠️ Browser tab |
| **Updates** | ⚠️ Manual | ✅ Auto-reload |

## Keyboard Shortcuts

| Key | Action |
|-----|--------|
| `Ctrl+O` | Open image (future) |
| `Ctrl+S` | Save image (future) |
| `Ctrl+Q` | Quit (future) |
| `F5` | Run detection (future) |

*Note: Shortcuts to be implemented in future version*

## Troubleshooting

### Application Won't Start

**Problem**: Double-clicking bat file shows error
**Solution**: 
1. Check Python installed: `python --version`
2. Reinstall Python with "Add to PATH" checked
3. Run as Administrator if needed

### "Tkinter not found"

**Problem**: Import error for tkinter
**Solution**:
- Windows: Reinstall Python, ensure "tcl/tk" is checked
- macOS: `brew install python-tk`
- Linux: `sudo apt-get install python3-tk`

### Models Not Found

**Problem**: ❌ Tree Model: Not Found
**Solution**:
1. Train models first:
   ```cmd
   python train_cpu.py
   python train_defects.py
   ```
2. Check `runs/` folder exists
3. Verify weights files exist:
   - `runs/detect/tree_detection_cpu/weights/best.pt`
   - `runs/defects/tree_defects_detection2/weights/best.pt`

### Slow Performance

**Problem**: Detection takes a long time
**Solution**:
- Normal on CPU (30-60 seconds per image)
- Use smaller images (resize before upload)
- Use GPU if available
- Close other applications

### Application Freezes

**Problem**: UI becomes unresponsive
**Solution**:
- Wait - detection is processing
- Progress bar should animate
- Check terminal for errors
- Restart application if truly frozen

### Image Won't Load

**Problem**: Error loading image
**Solution**:
- Check image format (JPG, PNG supported)
- Check image isn't corrupted
- Try different image
- Check file permissions

### Can't Save Results

**Problem**: Save buttons don't work
**Solution**:
- Run detection first
- Check write permissions
- Choose accessible folder
- Check disk space

## Technical Details

### Architecture
```python
TreeDetectionApp (Main Class)
├── UI Setup
│   ├── Left Panel (Controls)
│   ├── Right Panel (Results)
│   └── Status Bar
├── Model Loading (Threaded)
│   ├── Tree Detection Model
│   └── Defect Detection Model
├── Image Processing
│   ├── Load & Display
│   └── Scaling & Rendering
├── Detection (Threaded)
│   ├── Two-Stage Pipeline
│   ├── Visualization
│   └── Results Formatting
└── Export Functions
    ├── Save Image
    └── Save JSON
```

### Threading
- Model loading: Background thread
- Detection: Background thread
- UI: Main thread (always responsive)
- Progress: Indeterminate animation

### Memory Management
- Images cached in memory
- Results stored in session
- Automatic cleanup on new detection
- Canvas images properly referenced

## Customization

### Window Size
Edit `app_gui.py`:
```python
self.root.geometry("1400x900")  # Width x Height
self.root.minsize(1200, 800)    # Minimum size
```

### Default Confidence
Edit `app_gui.py`:
```python
self.tree_conf = tk.DoubleVar(value=0.25)    # Tree confidence
self.defect_conf = tk.DoubleVar(value=0.20)  # Defect confidence
```

### Colors & Themes
Standard Tkinter themes:
```python
style = ttk.Style()
style.theme_use('clam')  # or 'alt', 'default', 'classic'
```

## File Locations

```
Roboflow model/
├── app_gui.py                          ← Desktop application
├── start_desktop_app.bat              ← Windows launcher
├── start_desktop_app.sh               ← Unix launcher
├── two_stage_detection.py             ← Detection logic (shared)
└── runs/
    ├── detect/
    │   └── tree_detection_cpu/
    │       └── weights/best.pt        ← Tree model
    └── defects/
        └── tree_defects_detection2/
            └── weights/best.pt        ← Defect model
```

## Comparison: Web vs Desktop vs CLI

| Feature | Desktop | Web | CLI |
|---------|---------|-----|-----|
| **Interface** | Native GUI | Browser | Terminal |
| **Ease of Use** | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐ |
| **Setup** | One-click | Start server | Command |
| **Visual Feedback** | ✅ Rich | ✅ Rich | ⚠️ Limited |
| **Batch Processing** | ❌ Manual | ❌ Manual | ✅ Scripts |
| **Automation** | ❌ No | ⚠️ Limited | ✅ Full |
| **Resource Usage** | Low | Medium | Low |
| **Multi-User** | ❌ No | ✅ Yes | ❌ No |

## Best Use Cases

### Use Desktop App When:
- ✅ Single user, local processing
- ✅ Want native application feel
- ✅ Need offline operation
- ✅ Prefer click-and-drag workflow
- ✅ Windows environment

### Use Web App When:
- ✅ Multiple users need access
- ✅ Remote access required
- ✅ Cross-platform consistency
- ✅ Want hot-reload during development

### Use CLI When:
- ✅ Batch processing many images
- ✅ Automation/scripting needed
- ✅ Integration with other tools
- ✅ Server/headless environment

## Future Enhancements

Planned features:
- [ ] Keyboard shortcuts
- [ ] Drag-and-drop image loading
- [ ] Batch processing multiple images
- [ ] Real-time video detection
- [ ] Custom model selection
- [ ] Settings persistence
- [ ] Dark theme
- [ ] Zoom/pan on images
- [ ] Export to PDF report
- [ ] Statistics dashboard

## Support

### Issues
- Check terminal output for errors
- Verify Python and dependencies installed
- Ensure models are trained
- Check file permissions

### Getting Help
- See main README.md
- Check WINDOWS_GUIDE.md
- Review error messages carefully
- Test with simple images first

## License

Part of the Moscow-LCT project.
All model weights tracked with Git LFS.

---

**Ready to detect trees? Launch `start_desktop_app.bat` and start analyzing! 🌲**
