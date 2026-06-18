#!/usfrom ultralytics import YOLO
from pathlib import Path
import torch

# Fix for PyTorch 2.6+ weights_only security change
try:
    from ultralytics.nn.tasks import DetectionModel

    torch.serialization.add_safe_globals([DetectionModel])
except Exception:
    pass  # Older PyTorch versions don't have this python3
"""
Test the defect detection model directly to debug detection issues
"""

from ultralytics import YOLO
from pathlib import Path
import torch

# Fix for PyTorch 2.6+ weights_only security change
try:
    torch.serialization.add_safe_globals(["ultralytics.nn.tasks.DetectionModel"])
except Exception:
    pass  # Older PyTorch versions don't have this

# Load the defect model
print("Loading defect model...")
model = YOLO("runs/defects/tree_defects_detection2/weights/best.pt")

# Get model class names
print(f"\nModel classes ({len(model.names)}):")
for idx, name in model.names.items():
    print(f"  {idx}: {name}")

# Test on a training image
test_image = "defects/dataset/train/images/_Vr0_6HYzc4_jpg.rf.76846c2fdfa93cdbd1e5c43a851d2e9f.jpg"

if not Path(test_image).exists():
    print(f"\nError: Test image not found: {test_image}")
    exit(1)

print(f"\nRunning detection on: {test_image}")
print("Testing with different confidence thresholds...\n")

for conf in [0.05, 0.10, 0.15, 0.20, 0.25, 0.30]:
    results = model(test_image, conf=conf, verbose=False)
    boxes = results[0].boxes

    print(f"Confidence {conf:.2f}: {len(boxes)} detections")

    if len(boxes) > 0 and conf == 0.05:  # Show details for lowest threshold
        print("\n  Detections:")
        for box, cls, conf_val in zip(
            boxes.xyxy.cpu().numpy(), boxes.cls.cpu().numpy(), boxes.conf.cpu().numpy()
        ):
            class_name = model.names[int(cls)]
            print(f"    - {class_name}: {conf_val:.3f}")
        print()

# Save a visualization with very low threshold
print("\nGenerating visualization with conf=0.05...")
results = model(test_image, conf=0.05, verbose=False)
output_path = "test_defect_detection_output.jpg"
results[0].save(output_path)
print(f"Saved to: {output_path}")
print(f"\nTotal detections at 0.05 threshold: {len(results[0].boxes)}")
