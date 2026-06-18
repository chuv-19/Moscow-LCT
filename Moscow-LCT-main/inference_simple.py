#!/usrfrom ultralytics import YOLO
from pathlib import Path
import sys
import cv2
import torch
from config_loader import load_config

# Fix for PyTorch 2.6+ weights_only security change
try:
    from ultralytics.nn.tasks import DetectionModel

    torch.serialization.add_safe_globals([DetectionModel])
except Exception:
    pass  # Older PyTorch versions don't have thishon3
"""
YOLOv11 Simple Inference Script for Tree Detection
Command-line tool for running inference on images
"""

from ultralytics import YOLO
from pathlib import Path
import sys
import cv2
import torch
from config_loader import load_config

# Fix for PyTorch 2.6+ weights_only security change
try:
    torch.serialization.add_safe_globals(["ultralytics.nn.tasks.DetectionModel"])
except Exception:
    pass  # Older PyTorch versions don't have this

# Load configuration
config = load_config()


def find_latest_model():
    """Find the most recently trained model using config"""
    return config.get_model_path()


def run_inference(model_path, image_path, conf=0.25, save=True):
    """Run inference on an image"""
    # Load model
    print(f"Loading model: {model_path}")
    model = YOLO(model_path)

    # Run inference
    print(f"Running inference on: {image_path}")
    results = model(image_path, conf=conf, save=save, project="runs/predict")

    # Print results
    boxes = results[0].boxes
    num_detections = len(boxes)

    print(f"\n{'='*50}")
    print(f"Results:")
    print(f"{'='*50}")
    print(f"Detections: {num_detections} trees found")

    if num_detections > 0:
        confidences = boxes.conf.cpu().numpy()
        print(f"Confidence range: {confidences.min():.3f} - {confidences.max():.3f}")
        print(f"Average confidence: {confidences.mean():.3f}")

        print(f"\nDetailed detections:")
        for i, (box, conf) in enumerate(zip(boxes.xyxy.cpu().numpy(), confidences)):
            x1, y1, x2, y2 = box
            print(
                f"  Tree {i+1}: Confidence={conf:.3f}, BBox=[{x1:.0f}, {y1:.0f}, {x2:.0f}, {y2:.0f}]"
            )
    else:
        print("No trees detected above confidence threshold")

    if save:
        print(f"\nResult saved to: {results[0].save_dir}")

    print(f"{'='*50}\n")


def main():
    # Check arguments
    if len(sys.argv) < 2:
        print(
            "Usage: python inference_simple.py <image_path> [model_path] [confidence]"
        )
        print("\nExamples:")
        print("  python inference_simple.py test_image.jpg")
        print(
            "  python inference_simple.py test_image.jpg runs/detect/tree_detection_cpu/weights/best.pt"
        )
        print(
            "  python inference_simple.py test_image.jpg runs/detect/tree_detection_cpu/weights/best.pt 0.3"
        )

        # Try to find latest model and show example
        latest_model = find_latest_model()
        if latest_model:
            print(f"\nLatest trained model found: {latest_model}")

        sys.exit(1)

    image_path = sys.argv[1]

    # Get model path
    if len(sys.argv) >= 3:
        model_path = sys.argv[2]
    else:
        model_path = find_latest_model()
        if model_path is None:
            print(
                "Error: No trained model found. Please specify model path or train a model first."
            )
            sys.exit(1)
        print(f"Using latest model: {model_path}")

    # Get confidence threshold
    conf = float(sys.argv[3]) if len(sys.argv) >= 4 else 0.25

    # Check if files exist
    if not Path(image_path).exists():
        print(f"Error: Image not found: {image_path}")
        sys.exit(1)

    if not Path(model_path).exists():
        print(f"Error: Model not found: {model_path}")
        sys.exit(1)

    # Run inference
    run_inference(model_path, image_path, conf=conf)


if __name__ == "__main__":
    main()
