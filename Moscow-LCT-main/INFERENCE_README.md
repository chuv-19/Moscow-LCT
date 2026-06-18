# YOLOv11 Tree Detection - Inference Tools

This folder contains tools for running inference on images using your trained YOLOv11 tree detection model.

## Available Tools

### 1. GUI Inference Tool (`inference_gui.py`)
A user-friendly graphical interface for selecting and running inference on images.

**Features:**
- File picker for easy image selection
- Visual comparison of original vs. detected images
- Adjustable confidence threshold
- Detection statistics display
- Save results functionality
- Auto-loads the latest trained model

**Usage:**
```bash
python inference_gui.py
```

**Instructions:**
1. The GUI will automatically try to load your most recent trained model
2. Click "Select Image" to choose an image for detection
3. Adjust the confidence threshold if needed (default: 0.25)
4. Click "Run Detection" to process the image
5. View results side-by-side with detection statistics
6. Optionally save the result image

### 2. Command-Line Inference Tool (`inference_simple.py`)
A simple command-line tool for batch processing or quick inference.

**Usage:**
```bash
# Basic usage (uses latest model automatically)
python inference_simple.py path/to/image.jpg

# Specify model path
python inference_simple.py path/to/image.jpg runs/detect/tree_detection_cpu/weights/best.pt

# Specify confidence threshold
python inference_simple.py path/to/image.jpg runs/detect/tree_detection_cpu/weights/best.pt 0.3
```

**Examples:**
```bash
# Test on validation image
python inference_simple.py dataset/test/images/istockphoto-1057939746-612x612_jpg.rf.e29922376d27e544f472d4c5aa4cb073.jpg

# Use specific model with 30% confidence threshold
python inference_simple.py my_test_image.jpg runs/detect/tree_detection_cpu/weights/best.pt 0.30
```

## Model Locations

Trained models are saved in:
```
runs/detect/<experiment_name>/weights/
  ├── best.pt      # Best model based on validation metrics
  └── last.pt      # Last epoch checkpoint
```

Common experiment names:
- `tree_detection_cpu` - CPU-optimized training
- `tree_detection` - Full training configuration
- `tree_detection_simple` - Simple training script

## Requirements

All required packages are already installed in your virtual environment:
- ultralytics (YOLOv11)
- opencv-python
- pillow
- tkinter (usually comes with Python)

## Tips

### Confidence Threshold
- **Lower (0.1-0.3)**: Detects more trees but may include false positives
- **Medium (0.25-0.5)**: Balanced detection (recommended)
- **Higher (0.5-0.9)**: Only high-confidence detections, may miss some trees

### Best Practices
1. Use the **best.pt** model for inference (trained on validation performance)
2. Test on multiple images to understand model performance
3. Adjust confidence threshold based on your use case
4. For production, consider using GPU-trained models for better accuracy

## Output Format

### GUI Output
- Side-by-side comparison of original and detected images
- Detection count and confidence statistics
- Bounding boxes with confidence scores

### CLI Output
- Detection count
- Confidence statistics (min, max, average)
- Bounding box coordinates for each detection
- Saved result image in `runs/predict/`

## Troubleshooting

**Model not found:**
- Make sure you've completed training first
- Check that weights exist in `runs/detect/<experiment>/weights/best.pt`

**Image not loading:**
- Supported formats: JPG, PNG, BMP, GIF, TIFF
- Check file path and permissions

**Low detection accuracy:**
- Try adjusting confidence threshold
- Consider training for more epochs
- Use larger model (yolo11s, yolo11m) if needed

**GUI not opening:**
- Ensure tkinter is installed: `python -m tkinter`
- On macOS, may need to install: `brew install python-tk`

## Next Steps

To improve your model:
1. Train for more epochs (change `epochs=10` to `epochs=50+`)
2. Use a larger model size (yolo11s, yolo11m instead of yolo11n)
3. Collect more training data
4. Adjust data augmentation parameters

For questions or issues, refer to the Ultralytics documentation:
https://docs.ultralytics.com/
