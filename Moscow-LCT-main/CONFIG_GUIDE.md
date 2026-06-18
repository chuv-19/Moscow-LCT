# Configuration Guide for YOLOv11 Tree Detection

This guide explains how to configure the inference application using the `config.ini` file.

## Quick Start

The application automatically creates and uses a `config.ini` file in your project root. You can edit this file to customize paths and settings.

## Configuration File Location

```
/Users/hanqnero/Dev/Roboflow model/config.ini
```

## Configuration Sections

### 1. Model Configuration

```ini
[model]
# Path to your trained YOLO model
model_path = runs/detect/tree_detection_cpu/weights/best.pt
```

**Options:**
- Leave empty (`model_path = `) to auto-detect the latest trained model
- Use relative path from project root: `runs/detect/tree_detection_cpu/weights/best.pt`
- Use absolute path: `/full/path/to/model/best.pt`
- Use pretrained model: `yolo11n.pt` (will be downloaded automatically)

**Examples:**
```ini
# Auto-detect latest model (default)
model_path = 

# Use specific trained model
model_path = runs/detect/tree_detection_cpu/weights/best.pt

# Use a different training run
model_path = runs/detect/tree_detection_cpu2/weights/best.pt

# Use pretrained YOLO model
model_path = yolo11n.pt
```

### 2. Paths Configuration

```ini
[paths]
# Project root directory (auto-detected if empty)
project_root = /Users/hanqnero/Dev/Roboflow model

# Directory containing training runs
runs_directory = runs/detect

# Test images directory for examples
test_images_directory = dataset/test/images
```

**project_root**: The base directory for your project. Leave empty for auto-detection.

**runs_directory**: Where training outputs are saved (relative to project root).

**test_images_directory**: Directory with example images to display in the web UI (relative to project root).

### 3. Inference Settings

```ini
[inference]
# Default confidence threshold (0.0 - 1.0)
default_confidence = 0.25

# Minimum confidence threshold
min_confidence = 0.05

# Maximum confidence threshold  
max_confidence = 0.95

# Confidence step size in slider
confidence_step = 0.05
```

**default_confidence**: Initial confidence value when loading the app (0.0 - 1.0).

**min_confidence**: Minimum allowed confidence in the slider.

**max_confidence**: Maximum allowed confidence in the slider.

**confidence_step**: Step size for confidence adjustment.

**Confidence Threshold Guide:**
- **0.05 - 0.20**: Very sensitive, many detections (may include false positives)
- **0.25 - 0.40**: Balanced (recommended for most cases)
- **0.50 - 0.70**: Conservative, high confidence only
- **0.75 - 0.95**: Very strict, only highest confidence detections

### 4. Display Settings

```ini
[display]
# Maximum number of example images to show
max_example_images = 3

# Image display width (pixels)
default_image_width = 640
```

**max_example_images**: Number of example images shown in the web interface.

**default_image_width**: Default width for image display (in pixels).

## Usage Examples

### Example 1: Using a Specific Model

Edit `config.ini`:
```ini
[model]
model_path = runs/detect/tree_detection_cpu2/weights/best.pt
```

### Example 2: Adjusting Confidence Settings

For more sensitive detection:
```ini
[inference]
default_confidence = 0.15
min_confidence = 0.05
max_confidence = 0.50
confidence_step = 0.01
```

### Example 3: Using Different Test Images

```ini
[paths]
test_images_directory = my_custom_images
```

### Example 4: Multiple Model Configurations

Create different config files for different models:

**config_model1.ini**:
```ini
[model]
model_path = runs/detect/tree_detection_cpu/weights/best.pt
```

**config_model2.ini**:
```ini
[model]
model_path = runs/detect/tree_detection_gpu/weights/best.pt
```

Then specify which config to use when running:
```bash
# Default config.ini
python inference_simple.py image.jpg

# Or modify the code to load specific config
# In your script: config = load_config('config_model2.ini')
```

## Troubleshooting

### Model Not Found

**Problem**: Web app shows "No trained model found"

**Solutions:**
1. Check if the model file exists at the specified path
2. Verify the path is correct (relative to project root)
3. Try using absolute path
4. Leave `model_path` empty to auto-detect
5. Train a model first: `python train_cpu.py`

**Verify model exists:**
```bash
ls -la runs/detect/*/weights/best.pt
```

### Path Issues

**Problem**: Paths not resolving correctly

**Solutions:**
1. Use absolute paths for debugging
2. Check project_root is set correctly
3. Verify file/directory permissions
4. Use forward slashes (/) even on Windows

### Configuration Not Loading

**Problem**: Changes to config.ini not taking effect

**Solutions:**
1. Restart the application (Streamlit caches resources)
2. Clear Streamlit cache: Press 'C' in the web interface
3. Check for syntax errors in config.ini
4. Verify file is saved correctly

### Testing Configuration

Run the configuration tester:
```bash
python config_loader.py
```

This will display:
- Config file location
- Project root
- Model path (resolved)
- Test images directory
- All inference and display settings

## Advanced Usage

### Environment-Specific Configs

Create different configs for different environments:

**config.dev.ini**: Development settings
**config.prod.ini**: Production settings

Modify your scripts to load the appropriate config:
```python
import os
env = os.getenv('ENV', 'dev')
config = load_config(f'config.{env}.ini')
```

### Programmatic Configuration

You can also configure settings programmatically:

```python
from config_loader import Config

config = Config()
config.config.set('model', 'model_path', 'my_model.pt')
config.config.set('inference', 'default_confidence', '0.3')
config.save_config()
```

### Creating a New Config File

```python
from config_loader import Config

config = Config('my_config.ini')
config.create_default_config()
```

## Best Practices

1. **Version Control**: Commit a template config file, ignore the actual config:
   ```bash
   # Add to .gitignore
   config.ini
   
   # Keep template
   config.template.ini
   ```

2. **Documentation**: Comment your custom settings in config.ini

3. **Backup**: Keep backup of working configurations

4. **Testing**: Test config changes with `python config_loader.py`

5. **Validation**: The app validates paths and provides helpful error messages

## Need Help?

- Check if model file exists: `ls runs/detect/*/weights/best.pt`
- Test configuration: `python config_loader.py`
- View app logs in terminal when running Streamlit
- Check `INFERENCE_README.md` for general usage help

## Summary

The configuration file makes it easy to:
- ✅ Switch between different trained models
- ✅ Adjust detection sensitivity
- ✅ Customize UI behavior
- ✅ Manage different environments
- ✅ Share settings across team members

Just edit `config.ini` and restart the application!