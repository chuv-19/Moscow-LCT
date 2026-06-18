# 🌲 Tree Detection System

AI-powered tree and defect detection using YOLOv11.

---

## 🚀 Quick Start (New Users)

### One-Command Setup

**Mac/Linux:**
```bash
chmod +x setup.sh
./setup.sh
```

**Windows:**
```cmd
setup.bat
```

This installs everything you need in 5-10 minutes!

### Launch the App

**Mac/Linux:**
```bash
./start_mobile_app.sh
```

**Windows:**
```cmd
start_mobile_app.bat
```

**Access at:** http://localhost:8501

---

## 📱 Install on Phone (PWA)

### Step 1: Start with Network Access

```bash
./start_app_network.sh   # Mac/Linux
start_app_network.bat    # Windows
```

### Step 2: Connect from Phone

1. Find your IP: `ifconfig | grep "inet "` (Mac) or `ipconfig` (Windows)
2. On phone, go to: `http://YOUR_IP:8501`
3. Tap "Install app" in browser menu
4. App appears on home screen!

**Full guide:** See `PWA_GUIDE.md`

---

## 📚 Documentation

- **[QUICK_START_NEW_USER.md](QUICK_START_NEW_USER.md)** - Complete setup guide
- **[PWA_GUIDE.md](PWA_GUIDE.md)** - Phone installation guide
- **[CONFIG_GUIDE.md](CONFIG_GUIDE.md)** - Configuration options
- **[ARCHITECTURE.md](ARCHITECTURE.md)** - System architecture
- **[WINDOWS_GUIDE.md](WINDOWS_GUIDE.md)** - Windows-specific help
- **[CLEANUP_SUMMARY.md](CLEANUP_SUMMARY.md)** - Recent changes

---

## ✨ Features

### Detection Capabilities:
- 🌳 **Tree Detection:** Bush, Oak (2 classes)
- 🔍 **Defect Detection:** 12 defect types
  - Crack, Dead Bush, Dead Tree, Dry Crown
  - Leaned Tree, Marked Tree, Rot
  - Stem Damage, Stem Rot, Tree Hole
  - And more...

### User Interfaces:
- 📱 **PWA (Mobile):** Install on phone like native app
- 🖥️ **Web App:** Desktop browser interface
- 🪟 **Desktop GUI:** Tkinter native application

### Deployment Options:
- 🏠 **Local:** Run on localhost
- 📡 **Network:** Access from phone/tablet
- ☁️ **Cloud:** Deploy to Streamlit Cloud (optional)

---

## 🎯 System Requirements

- **Python:** 3.8 or higher
- **Disk Space:** 2GB minimum
- **RAM:** 4GB minimum (8GB recommended)
- **OS:** macOS, Linux, or Windows

---

## 📁 Project Structure

```
.
├── setup.sh / setup.bat         # 👈 Run this first!
├── requirements.txt             # Python dependencies
│
├── app_mobile.py                # PWA web app (Russian)
├── start_mobile_app.sh/bat      # Launch PWA
├── start_app_network.sh/bat     # Launch with network
│
├── two_stage_detection.py       # Core detection logic
├── config.ini                   # Configuration
│
├── runs/                        # Trained models
│   ├── detect/                  # Tree models
│   └── defects/                 # Defect models
│
└── dataset/                     # Training data
```

---

## 🏋️ Training Models

### Train Tree Detection:
```bash
./train_trees.bat
```

### Train Defect Detection:
```bash
./train_defects.bat
```

Models are saved to `runs/` directory.

---

## 🔧 Configuration

Edit `config.ini` to customize:
- Model paths
- Confidence thresholds
- Image sizes
- And more...

See `CONFIG_GUIDE.md` for details.

---

## 💻 Development

### Project Components:

**Core:**
- `two_stage_detection.py` - Detection pipeline
- `config_loader.py` - Configuration management

**Interfaces:**
- `app_mobile.py` - PWA (mobile-optimized)
- `app.py` - Main web app
- `app_gui.py` - Desktop GUI
- `two_stage_web.py` - Alternative web UI

**Training:**
- `train_trees.py` - Tree model training
- `train_defects.py` - Defect model training
- `train_cpu.py` - CPU-optimized training

---

## 🌐 Tech Stack

- **Deep Learning:** PyTorch 2.8.0
- **Object Detection:** Ultralytics YOLOv11n
- **Web Framework:** Streamlit 1.28+
- **Image Processing:** OpenCV 4.8+
- **Desktop GUI:** Tkinter
- **Language:** Python 3.13

---

## 🎨 Usage Examples

### 1. Quick Local Test
```bash
./start_mobile_app.sh
# Upload image → Click detect → View results
```

### 2. Team Deployment
```bash
./start_app_network.sh
# Share IP with team on same WiFi
```

### 3. Field Work
```bash
./start_app_network.sh
# Install PWA on phone
# Use camera to capture and analyze trees
```

---

## 🐛 Troubleshooting

### Installation Issues

**"Python not found"**
```bash
# Install Python 3.8+ from python.org
```

**"Permission denied"**
```bash
chmod +x setup.sh
./setup.sh
```

### Runtime Issues

**"Model not found"**
```bash
# Train models first
./train_trees.bat
./train_defects.bat
```

**"Port already in use"**
```bash
# Kill process on port 8501
lsof -ti:8501 | xargs kill -9
```

**Phone can't connect**
- Check same WiFi network
- Verify IP address
- Check firewall settings
- Use `http://` not `https://`

See `QUICK_START_NEW_USER.md` for more solutions.

---

## 📊 Model Performance

### Tree Detection:
- **Classes:** Bush, Oak
- **Input Size:** 640x640
- **Model:** YOLOv11n (2.6M params)

### Defect Detection:
- **Classes:** 12 defect types
- **Input Size:** 640x640
- **Model:** YOLOv11n (2.6M params)

Performance varies by image quality and conditions.

---

## 🤝 Contributing

This is a working production system. Improvements welcome!

### Areas for Enhancement:
- Additional tree species
- More defect types
- Performance optimization
- UI improvements
- Documentation

---

## 📝 License

[Your License Here]

---

## 🙏 Acknowledgments

- **Ultralytics** - YOLOv11 framework
- **Streamlit** - Web framework
- **PyTorch** - Deep learning platform

---

## 📞 Support

**Documentation:**
- Quick Start: `QUICK_START_NEW_USER.md`
- PWA Guide: `PWA_GUIDE.md`
- Configuration: `CONFIG_GUIDE.md`

**Issues:** Check troubleshooting sections in docs

---

## 🎯 Quick Reference

```bash
# Setup (one time)
./setup.sh

# Run locally
./start_mobile_app.sh

# Run with network access
./start_app_network.sh

# Train models
./train_trees.bat
./train_defects.bat

# Find IP for phone access
ifconfig | grep "inet " | grep -v 127.0.0.1
```

---

**Made with ❤️ for forest health monitoring**

🌲 Happy tree detecting!
