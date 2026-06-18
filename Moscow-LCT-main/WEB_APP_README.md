# Web App Quick Start

## Launch the Main Application

Simply run:
```bash
streamlit run app.py
```

This will open a web interface at `http://localhost:8501` where you can:
- Check model status
- Choose between Simple Tree Detection or Two-Stage Detection
- Access quick start guides and documentation

## Direct Access to Applications

### Simple Tree Detection
```bash
streamlit run inference_web.py
```

### Two-Stage Detection (Trees + Defects)
```bash
streamlit run two_stage_web.py
```

## First Time Setup

1. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Train models** (if not already done):
   ```bash
   python train_cpu.py          # Tree detection model
   python train_defects.py      # Defect detection model (40 epochs)
   ```

3. **Launch the app:**
   ```bash
   streamlit run app.py
   ```

## Application Features

### 🌳 Simple Tree Detection (`inference_web.py`)
- Single-stage tree detection
- Fast processing
- Basic tree counting
- Ideal for quick analysis

### 🔍 Two-Stage Detection (`two_stage_web.py`)
- Advanced tree detection
- Tree type identification (bush, oak)
- 12 defect types detection
- Tree-defect association
- Comprehensive health analysis

## Model Information

- **Tree Detection Model**: `runs/detect/tree_detection_cpu/weights/best.pt`
- **Defect Detection Model**: `runs/defects/tree_defects_detection/weights/best.pt`

Both models use YOLOv11n architecture optimized for CPU inference.

## Command-Line Alternative

If you prefer command-line tools:

```bash
# Simple detection
python inference_simple.py image.jpg

# Two-stage detection
python two_stage_detection.py image.jpg
```

## Troubleshooting

**Models not found?**
- Run the training scripts first (see step 2 above)
- Check that models exist in the `runs/` directory

**Port already in use?**
- Streamlit uses port 8501 by default
- Use `streamlit run app.py --server.port 8502` to use a different port

**Import errors?**
- Make sure all dependencies are installed
- Activate your virtual environment if using one
