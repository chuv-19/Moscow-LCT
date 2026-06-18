#!/usr/bin/env python3
"""
YOLOv11 Training Script for Tree Defect Detection
Trains on the defects dataset with 14 classes (tree types + defects)
"""

from ultralytics import YOLO
import torch
from pathlib import Path
import os


def main():
    # Get the script directory
    script_dir = Path(__file__).parent.resolve()
    print(f"PyTorch version: {torch.__version__}")
    print(f"CUDA available: {torch.cuda.is_available()}")

    if torch.cuda.is_available():
        print(f"CUDA device count: {torch.cuda.device_count()}")
        device = "0"
    else:
        print("Using CPU for training")
        device = "cpu"

    # Path to defects dataset (relative to script location)
    data_yaml = script_dir / "defects" / "dataset" / "data.yaml"

    print(f"\nUsing dataset: {data_yaml}")
    print(f"\n14 Classes:")
    print(
        f"  bush, crack, dead_bush, deadtree, dry_crone, leaned_tree, marked_tree, markedtree, markettree, oak, rot, stem_damage, stem_rot, tree_hole"
    )

    # Initialize YOLOv11 nano model
    print(f"\nInitializing YOLOv11n model...")
    model = YOLO("yolo11n.pt")

    # Training parameters optimized for CPU
    print(f"\nStarting training...")
    results = model.train(
        data=data_yaml,
        epochs=40,  # More epochs for complex dataset
        imgsz=640,  # Larger images for defect detection
        batch=8,  # Moderate batch size
        device=device,
        project="runs/defects",
        name="tree_defects_detection",
        workers=4,
        patience=10,
        cache=False,
        amp=False if device == "cpu" else True,
        verbose=True,
        seed=0,
        deterministic=True,
        split=0.8,  # Use 80% train, 20% val split since only train folder exists
        # Data augmentation
        hsv_h=0.015,
        hsv_s=0.7,
        hsv_v=0.4,
        degrees=0.0,
        translate=0.1,
        scale=0.5,
        shear=0.0,
        perspective=0.0,
        flipud=0.0,
        fliplr=0.5,
        mosaic=1.0,
        mixup=0.0,
    )

    print(f"\nTraining completed!")
    print(f"Results saved in: {results.save_dir}")

    # Validate the model with the same dataset
    print(f"\nValidating the model...")
    val_results = model.val(data=data_yaml, split="val")

    print(f"\nValidation completed!")
    print(f"Model ready for two-stage detection (trees + defects)")


if __name__ == "__main__":
    main()
