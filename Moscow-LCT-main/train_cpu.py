#!/usr/bin/env python3
"""
YOLOv11 Training Script for Tree Detection (CPU Optimized)
"""

from ultralytics import YOLO
import torch
from pathlib import Path

# Get the script directory
script_dir = Path(__file__).parent.resolve()

print(f"PyTorch version: {torch.__version__}")
print(f"CUDA available: {torch.cuda.is_available()}")
if torch.cuda.is_available():
    print(f"CUDA device count: {torch.cuda.device_count()}")
    device = "0"  # Use first GPU
else:
    print("Using CPU for training")
    device = "cpu"

# Initialize a YOLOv11 nano model (smallest/fastest)
model = YOLO("yolo11n.pt")

# Path to dataset (relative to script location)
data_yaml = script_dir / "dataset" / "data.yaml"

# Train the model with CPU-optimized settings
results = model.train(
    data=str(data_yaml),
    epochs=10,  # Reduced epochs for faster training on CPU
    imgsz=416,  # Smaller image size for faster training
    batch=4,  # Smaller batch size for CPU
    device=device,  # Use detected device
    project="runs/detect",
    name="tree_detection_cpu",
    workers=2,  # Fewer workers for CPU
    patience=5,  # Early stopping
    cache=False,  # Don't cache on CPU
    amp=False,  # Disable AMP on CPU
    verbose=True,
)

print("Training completed!")
print(f"Results saved in: {results.save_dir}")

# Quick validation
print("\nRunning validation...")
val_results = model.val()
print(f"Validation completed!")
