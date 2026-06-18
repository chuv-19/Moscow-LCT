# YOLOv11 Tree Detection - System Architecture

## System Overview

```
┌─────────────────────────────────────────────────────────────────┐
│                     YOLOv11 Tree Detection System                │
└─────────────────────────────────────────────────────────────────┘

┌──────────────┐      ┌──────────────┐      ┌──────────────┐
│   Dataset    │ ───> │   Training   │ ───> │    Model     │
│ (Images +    │      │  (train_*.py)│      │  (best.pt)   │
│  Labels)     │      └──────────────┘      └──────────────┘
└──────────────┘                                     │
                                                     │
                                                     ▼
                                            ┌──────────────┐
                                            │  config.ini  │
                                            │ (Model Path) │
                                            └──────────────┘
                                                     │
                           ┌─────────────────────────┼──────────────────────────┐
                           │                         │                          │
                           ▼                         ▼                          ▼
                  ┌────────────────┐       ┌────────────────┐        ┌────────────────┐
                  │  Web Interface │       │  CLI Tool      │        │  Desktop GUI   │
                  │ (Streamlit)    │       │ (Simple)       │        │  (Tkinter)     │
                  │ Port: 8501     │       │ Terminal       │        │  Optional      │
                  └────────────────┘       └────────────────┘        └────────────────┘
                           │                         │                          │
                           └─────────────────────────┼──────────────────────────┘
                                                     │
                                                     ▼
                                            ┌──────────────┐
                                            │  Inference   │
                                            │  Results     │
                                            └──────────────┘
```

## Component Details

### 1. Input Layer
```
Dataset (dataset/)
├── train/images/        # 2,221 training images
├── valid/images/        # 1,399 validation images
├── test/images/         # Test images for evaluation
└── data.yaml            # Dataset configuration
```

### 2. Training Layer
```
Training Scripts
├── train_cpu.py         # CPU-optimized (10 epochs, 416px)
├── train_simple.py      # Basic training
└── train_yolov11.py     # Full configuration (50 epochs)
```

### 3. Model Layer
```
Trained Models (runs/detect/)
├── tree_detection_cpu/
│   └── weights/
│       ├── best.pt      # Best performing model ⭐
│       └── last.pt      # Last checkpoint
└── [other experiments]/
    └── weights/
        └── best.pt
```

### 4. Configuration Layer
```
Configuration System
├── config.ini           # User-editable settings
│   ├── [model]         # Model path
│   ├── [paths]         # Directory paths
│   ├── [inference]     # Detection settings
│   └── [display]       # UI settings
│
└── config_loader.py     # Configuration manager
    ├── load_config()
    ├── find_latest_model()
    └── get_settings()
```

### 5. Inference Layer
```
Inference Tools
├── inference_web.py     # 🌐 Web GUI (Streamlit)
│   ├── File picker
│   ├── Confidence slider
│   ├── Side-by-side view
│   └── Download results
│
├── inference_simple.py  # 💻 CLI Tool
│   ├── Quick detection
│   ├── Batch processing
│   └── Auto model detection
│
└── inference_gui.py     # 🖥️ Desktop GUI (Tkinter)
    └── (Requires tkinter)
```

## Data Flow

### Training Flow
```
1. Load Dataset
   ↓
2. Initialize YOLO Model (yolo11n.pt)
   ↓
3. Train (N epochs)
   ↓
4. Validate Each Epoch
   ↓
5. Save Best Model (best.pt)
   ↓
6. Final Validation
   ↓
7. Export Results
```

### Inference Flow
```
1. Load config.ini
   ↓
2. Find/Load Model (best.pt)
   ↓
3. User Selects Image
   ↓
4. Set Confidence Threshold
   ↓
5. Run YOLO Inference
   ↓
6. Draw Bounding Boxes
   ↓
7. Calculate Statistics
   ↓
8. Display Results
   ↓
9. Optional: Save Output
```

## Configuration Flow

```
┌─────────────┐
│ config.ini  │
│ (User Edit) │
└──────┬──────┘
       │
       ▼
┌─────────────────┐
│ config_loader.py│
│ • Parse INI     │
│ • Validate      │
│ • Resolve Paths │
└──────┬──────────┘
       │
       ├──────────────────┐
       │                  │
       ▼                  ▼
┌─────────────┐   ┌──────────────┐
│ Web GUI     │   │ CLI Tool     │
│ Load Model  │   │ Load Model   │
│ Get Settings│   │ Get Settings │
└─────────────┘   └──────────────┘
```

## File Relationships

```
Project Root
│
├── Config Files
│   ├── config.ini ─────────────┐
│   └── config_loader.py ◄──────┤
│                               │
├── Inference Tools             │
│   ├── inference_web.py ◄──────┤
│   ├── inference_simple.py ◄───┤
│   └── inference_gui.py ◄──────┘
│
├── Training Scripts
│   ├── train_cpu.py ──┐
│   ├── train_simple.py ├─────> runs/detect/*/weights/best.pt
│   └── train_yolov11.py┘              ▲
│                                      │
├── Dataset                            │
│   └── data.yaml ──────────────────┘ │
│                                      │
└── Documentation                      │
    ├── SETUP_COMPLETE.md              │
    ├── CONFIG_GUIDE.md                │
    └── INFERENCE_README.md            │
```

## User Interaction Flow

### Web Interface
```
User Action                    System Response
───────────                    ─────────────────
1. Start app              ->   Load config.ini
                               Load model from config
                               Show interface

2. Upload image           ->   Display original image
                               Enable detection button

3. Adjust confidence      ->   Update threshold value
   slider                      (0.05 - 0.95)

4. Click "Run Detection"  ->   Process image
                               Draw bounding boxes
                               Calculate stats

5. View results           ->   Show detected image
                               Display count & confidence
                               Show detailed list

6. Download result        ->   Save annotated image
                               (JPEG format)
```

### CLI Tool
```
Command                              Output
─────────                            ──────
python inference_simple.py img.jpg

1. Load config                 ->    "Using latest model: ..."
2. Load model                  ->    "Loading model: ..."
3. Run inference               ->    "Running inference..."
4. Display results             ->    "Detections: N trees found"
5. Show statistics             ->    Confidence range & details
6. Save output                 ->    "Result saved to: ..."
```

## State Management

### Configuration State
```
config.ini (Persistent)
    ↓
config_loader.py (Runtime)
    ↓
Application (In-Memory)
    ↓
User Changes (Temporary)
    ↓
[Optional: Save to config.ini]
```

### Model State
```
Disk (best.pt)
    ↓
@st.cache_resource (Web GUI)
    ↓
Memory (Loaded Model)
    ↓
Inference (Active)
```

### Session State (Web GUI)
```
Page Load
    ↓
Load Config
    ↓
Load Model (Cached)
    ↓
User Session
│   ├── Upload Image (Temporary)
│   ├── Adjust Settings (Temporary)
│   └── Run Detection (Temporary)
    ↓
Clear on Refresh
```

## Error Handling Flow

```
Try Load Config
    ├─ Success: Continue
    └─ Fail: Use Defaults
           ↓
Try Load Model
    ├─ Success: Continue
    ├─ Not Found: Show Warning
    │              Display Config Help
    └─ Error: Show Error Message
              Allow Manual Selection
           ↓
Try Load Image
    ├─ Success: Display & Enable Detection
    └─ Fail: Show Error
             Request New Upload
           ↓
Try Run Inference
    ├─ Success: Show Results
    └─ Fail: Show Error
             Keep Original Image
```

## Performance Considerations

### Training (CPU)
```
Model Size    Images/sec    Memory    Training Time (10 epochs)
──────────    ──────────    ──────    ─────────────────────────
yolo11n       1.6 it/s      ~2GB      ~50-60 minutes
yolo11s       1.0 it/s      ~3GB      ~90 minutes
yolo11m       0.5 it/s      ~5GB      ~3 hours
```

### Inference (CPU)
```
Model Size    Time/Image    Accuracy    Use Case
──────────    ──────────    ────────    ────────
yolo11n       ~30ms         Lower       Fast preview
yolo11s       ~50ms         Medium      Balanced
yolo11m       ~100ms        Higher      Production
```

## Integration Points

### Easy Integrations
```
1. REST API
   └─> Wrap inference_simple.py in Flask/FastAPI

2. Batch Processing
   └─> Loop inference_simple.py over directory

3. Video Processing
   └─> Extract frames + run inference

4. Cloud Deployment
   └─> Docker container with Streamlit

5. Mobile Integration
   └─> Upload to web interface from mobile
```

### Code Integration Example
```python
from config_loader import load_config
from ultralytics import YOLO

# Load configuration
config = load_config()

# Get model path from config
model_path = config.get_model_path()

# Load model
model = YOLO(model_path)

# Run inference
results = model('image.jpg', conf=0.25)

# Process results
for result in results:
    boxes = result.boxes
    print(f"Found {len(boxes)} trees")
```

## Summary

This system provides:
- ✅ Flexible configuration via INI file
- ✅ Multiple inference interfaces (Web, CLI, GUI)
- ✅ Automatic model detection
- ✅ Adjustable confidence thresholds
- ✅ Visual and statistical results
- ✅ Easy customization and extension

The modular design allows you to:
- Switch models easily (edit config.ini)
- Adjust settings without code changes
- Choose your preferred interface
- Integrate with other systems
- Scale for production use