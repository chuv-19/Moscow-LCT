# YOLOv11 Tree Detection - Quick Start Guide

## ✅ Setup Complete!

Your YOLOv11 tree detection system is now configured and ready to use.

## 🚀 Running the Inference GUI

### Web Interface (Recommended)
```bash
python -m streamlit run inference_web.py
```

Then open your browser to: **http://localhost:8501**

Features:
- 🖼️ Simple file picker to select images
- 🎯 Visual side-by-side comparison
- 🎚️ Adjustable confidence threshold
- 📊 Detection statistics
- 💾 Download results
- 🌲 Example images from your dataset

### Command Line Interface
```bash
# Auto-detect latest model
python inference_simple.py path/to/image.jpg

# Specify model and confidence
python inference_simple.py image.jpg runs/detect/tree_detection_cpu/weights/best.pt 0.3
```

## ⚙️ Configuration

Your model and settings are configured in `config.ini`:

```ini
[model]
model_path = runs/detect/tree_detection_cpu/weights/best.pt

[inference]
default_confidence = 0.25
```

### Quick Configuration Changes

**Change model:**
```ini
model_path = runs/detect/another_model/weights/best.pt
```

**Adjust default confidence:**
```ini
default_confidence = 0.30
```

**Auto-detect latest model (leave empty):**
```ini
model_path = 
```

After editing `config.ini`, restart the web app.

## 📁 Files Created

| File | Purpose |
|------|---------|
| `config.ini` | Configuration file for model path and settings |
| `config_loader.py` | Configuration management module |
| `inference_web.py` | Web-based GUI (Streamlit) |
| `inference_simple.py` | Command-line inference tool |
| `inference_gui.py` | Tkinter GUI (may need tkinter installed) |
| `CONFIG_GUIDE.md` | Detailed configuration documentation |
| `INFERENCE_README.md` | Inference tools documentation |

## 🎯 Current Configuration Status

✅ **Model Found:** `runs/detect/tree_detection_cpu/weights/best.pt`
✅ **Test Images:** `dataset/test/images`
✅ **Default Confidence:** 0.25

## 📖 Documentation

- **Configuration Help:** See `CONFIG_GUIDE.md`
- **Inference Tools:** See `INFERENCE_README.md`
- **Training Help:** See training scripts (`train_cpu.py`, etc.)

## 🔧 Common Tasks

### Test Configuration
```bash
python config_loader.py
```

### View Available Models
```bash
ls -la runs/detect/*/weights/best.pt
```

### Change to Different Model
1. Edit `config.ini`
2. Update `model_path` line
3. Restart web app

### Test Single Image
```bash
python inference_simple.py dataset/test/images/sample.jpg
```

### Run Web Interface
```bash
python -m streamlit run inference_web.py
```

## 🌐 Web Interface Access

Once started, access at:
- **Local:** http://localhost:8501
- **Network:** Check terminal output for network URL

## 💡 Tips

1. **Model Not Found?**
   - Check `config.ini` path is correct
   - Run `python config_loader.py` to verify
   - Try leaving `model_path` empty to auto-detect

2. **Web App Not Starting?**
   - Check if port 8501 is available
   - Try: `python -m streamlit run inference_web.py --server.port=8502`

3. **Poor Detection Results?**
   - Lower confidence threshold (try 0.15-0.20)
   - Train for more epochs
   - Use larger model (yolo11s, yolo11m)

4. **Change Settings Without Editing File?**
   - Use web interface sliders for confidence
   - For permanent changes, edit `config.ini`

## 🎓 Next Steps

1. **Test the web interface** with your own images
2. **Adjust confidence threshold** to find optimal setting
3. **Train longer** for better accuracy (increase epochs in `train_cpu.py`)
4. **Try different model sizes** (yolo11s.pt, yolo11m.pt for better accuracy)

## 📊 Your Model Performance

Your trained model achieved:
- **mAP50:** ~0.386 (38.6% accuracy at 50% IoU threshold)
- **Trained on:** 2,221 images
- **Validated on:** 1,399 images
- **Classes:** 1 (trees)

For better results, consider training longer or with more data.

## 🆘 Need Help?

1. Check `CONFIG_GUIDE.md` for configuration issues
2. Check `INFERENCE_README.md` for usage help
3. Run `python config_loader.py` to verify configuration
4. Check terminal output for error messages

---

**Ready to detect trees! 🌲** Open http://localhost:8501 to get started.