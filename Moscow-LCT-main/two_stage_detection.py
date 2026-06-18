#!/usr/bin/env python3
"""
Two-Stage Tree and Defect Detection System
1. Detects trees using the tree detection model
2. Detects defects using the defect detection model
3. Maps defects to trees and provides structured output
"""

from ultralytics import YOLO
import cv2
import numpy as np
from pathlib import Path
from typing import List, Dict, Tuple
import json
import torch

# Fix for PyTorch 2.6+ weights_only security change
# Allow YOLO model classes to be loaded
try:
    from ultralytics.nn.tasks import DetectionModel

    torch.serialization.add_safe_globals([DetectionModel])
except Exception:
    pass  # Older PyTorch versions don't have this


class TwoStageDetector:
    """Two-stage detector for trees and their defects"""

    def __init__(self, tree_model_path: str, defect_model_path: str):
        """
        Initialize the two-stage detector

        Args:
            tree_model_path: Path to trained tree detection model
            defect_model_path: Path to trained defect detection model
        """
        print(f"Loading tree detection model: {tree_model_path}")
        self.tree_model = YOLO(tree_model_path)

        print(f"Loading defect detection model: {defect_model_path}")
        self.defect_model = YOLO(defect_model_path)

        # Define which classes are tree types vs defects
        # Based on the updated defects dataset classes (14 classes)
        self.tree_classes = {
            "bush",
            "oak",
        }

        self.defect_classes = {
            "crack",
            "dead_bush",
            "deadtree",
            "dry_crone",
            "leaned_tree",
            "marked_tree",  # Note: updated from markedtree
            "markedtree",
            "markettree",
            "rot",
            "stem_damage",
            "stem_rot",
            "tree_hole",
        }

    def calculate_iou(self, box1: List[float], box2: List[float]) -> float:
        """Calculate Intersection over Union between two boxes"""
        x1_1, y1_1, x2_1, y2_1 = box1
        x1_2, y1_2, x2_2, y2_2 = box2

        # Calculate intersection
        x1_i = max(x1_1, x1_2)
        y1_i = max(y1_1, y1_2)
        x2_i = min(x2_1, x2_2)
        y2_i = min(y2_1, y2_2)

        if x2_i < x1_i or y2_i < y1_i:
            return 0.0

        intersection = (x2_i - x1_i) * (y2_i - y1_i)

        # Calculate union
        area1 = (x2_1 - x1_1) * (y2_1 - y1_1)
        area2 = (x2_2 - x1_2) * (y2_2 - y1_2)
        union = area1 + area2 - intersection

        return intersection / union if union > 0 else 0.0

    def box_contains(
        self, outer_box: List[float], inner_box: List[float], threshold: float = 0.3
    ) -> bool:
        """Check if inner_box is inside or significantly overlaps with outer_box"""
        iou = self.calculate_iou(outer_box, inner_box)

        # Also check if defect center is inside tree box
        defect_center_x = (inner_box[0] + inner_box[2]) / 2
        defect_center_y = (inner_box[1] + inner_box[3]) / 2

        inside = (
            outer_box[0] <= defect_center_x <= outer_box[2]
            and outer_box[1] <= defect_center_y <= outer_box[3]
        )

        return iou > threshold or inside

    def detect(
        self, image_path: str, tree_conf: float = 0.25, defect_conf: float = 0.05
    ) -> Dict:
        """
        Run two-stage detection on an image

        Args:
            image_path: Path to input image
            tree_conf: Confidence threshold for tree detection
            defect_conf: Confidence threshold for defect detection (default 0.05 due to low model mAP)

        Returns:
            Dictionary containing trees and their associated defects
        """
        print(f"\n{'='*60}")
        print(f"Processing: {Path(image_path).name}")
        print(f"{'='*60}")

        # Stage 1: Detect trees using simple tree model
        print(f"\nStage 1: Detecting trees...")
        tree_results = self.tree_model(image_path, conf=tree_conf, verbose=False)

        trees = []
        tree_boxes = tree_results[0].boxes

        for idx, (box, conf) in enumerate(
            zip(tree_boxes.xyxy.cpu().numpy(), tree_boxes.conf.cpu().numpy())
        ):
            tree_id = f"Tree_{idx + 1}"
            trees.append(
                {
                    "id": tree_id,
                    "type": "tree",  # Simple tree model only detects trees
                    "bbox": box.tolist(),
                    "confidence": float(conf),
                    "defects": [],
                }
            )

        print(f"  Found {len(trees)} trees")

        # Stage 2: Detect defects and tree types using defect model
        print(f"\nStage 2: Detecting defects and tree types...")
        defect_results = self.defect_model(image_path, conf=defect_conf, verbose=False)

        defect_boxes = defect_results[0].boxes
        class_names = self.defect_model.names

        # Separate detections into tree types and defects
        tree_type_detections = []
        defect_detections = []

        for box, conf, cls in zip(
            defect_boxes.xyxy.cpu().numpy(),
            defect_boxes.conf.cpu().numpy(),
            defect_boxes.cls.cpu().numpy(),
        ):
            class_name = class_names[int(cls)]

            detection = {
                "class": class_name,
                "bbox": box.tolist(),
                "confidence": float(conf),
            }

            if class_name in self.tree_classes:
                tree_type_detections.append(detection)
            elif class_name in self.defect_classes:
                defect_detections.append(detection)

        print(f"  Found {len(tree_type_detections)} tree type identifications")
        print(f"  Found {len(defect_detections)} defects")

        # Stage 3: Map tree types to trees
        print(f"\nStage 3: Mapping tree types to trees...")
        for tree in trees:
            tree_bbox = tree["bbox"]
            best_match = None
            best_iou = 0.0

            for tree_type_det in tree_type_detections:
                iou = self.calculate_iou(tree_bbox, tree_type_det["bbox"])
                if iou > best_iou and iou > 0.3:
                    best_iou = iou
                    best_match = tree_type_det

            if best_match:
                tree["type"] = best_match["class"]
                tree["type_confidence"] = best_match["confidence"]

        # Stage 4: Map defects to trees
        print(f"\nStage 4: Mapping defects to trees...")
        unmatched_defects = []

        for defect in defect_detections:
            defect_bbox = defect["bbox"]
            matched = False

            # Find which tree(s) contain this defect
            for tree in trees:
                if self.box_contains(tree["bbox"], defect_bbox):
                    tree["defects"].append(
                        {
                            "type": defect["class"],
                            "confidence": defect["confidence"],
                            "bbox": defect["bbox"],
                        }
                    )
                    matched = True

            if not matched:
                unmatched_defects.append(defect)

        # Summary
        results = {
            "image": str(image_path),
            "total_trees": len(trees),
            "total_defects": len(defect_detections),
            "trees": trees,
            "unmatched_defects": unmatched_defects,
        }

        return results

    def print_results(self, results: Dict):
        """Print detection results in a readable format"""
        print(f"\n{'='*60}")
        print(f"DETECTION RESULTS")
        print(f"{'='*60}")
        print(f"Image: {Path(results['image']).name}")
        print(f"Total Trees: {results['total_trees']}")
        print(f"Total Defects: {results['total_defects']}")
        print(f"{'='*60}\n")

        if not results["trees"]:
            print("No trees detected.")
            return

        for tree in results["trees"]:
            print(f"┌─ {tree['id']}")
            print(f"│  Type: {tree['type']}")
            print(f"│  Confidence: {tree['confidence']:.3f}")
            if "type_confidence" in tree:
                print(f"│  Type Confidence: {tree['type_confidence']:.3f}")

            x1, y1, x2, y2 = tree["bbox"]
            print(f"│  BBox: [{x1:.0f}, {y1:.0f}, {x2:.0f}, {y2:.0f}]")

            if tree["defects"]:
                print(f"│  Defects ({len(tree['defects'])}):")
                for i, defect in enumerate(tree["defects"], 1):
                    print(
                        f"│    {i}. {defect['type']} (conf: {defect['confidence']:.3f})"
                    )
            else:
                print(f"│  Defects: None ✓")

            print(f"└{'─'*58}\n")

        if results["unmatched_defects"]:
            print(f"⚠ Unmatched Defects ({len(results['unmatched_defects'])}):")
            for defect in results["unmatched_defects"]:
                print(f"  - {defect['class']} (conf: {defect['confidence']:.3f})")
            print()

    def visualize(self, image_path: str, results: Dict, output_path: str = None):
        """
        Create visualization of detection results

        Args:
            image_path: Path to original image
            results: Detection results dictionary
            output_path: Path to save visualization (optional)
        """
        img = cv2.imread(str(image_path))

        # Color scheme
        tree_color = (0, 255, 0)  # Green for trees
        defect_color = (0, 0, 255)  # Red for defects

        # Draw trees
        for tree in results["trees"]:
            x1, y1, x2, y2 = [int(v) for v in tree["bbox"]]

            # Draw tree bounding box
            cv2.rectangle(img, (x1, y1), (x2, y2), tree_color, 3)

            # Label
            label = f"{tree['id']}: {tree['type']}"
            cv2.putText(
                img, label, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.6, tree_color, 2
            )

            # Draw defects within this tree
            for defect in tree["defects"]:
                dx1, dy1, dx2, dy2 = [int(v) for v in defect["bbox"]]
                cv2.rectangle(img, (dx1, dy1), (dx2, dy2), defect_color, 2)

                defect_label = f"{defect['type'][:10]}"
                cv2.putText(
                    img,
                    defect_label,
                    (dx1, dy1 - 5),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.4,
                    defect_color,
                    1,
                )

        if output_path is None:
            output_path = Path(image_path).stem + "_detected.jpg"

        cv2.imwrite(str(output_path), img)
        print(f"\nVisualization saved to: {output_path}")

        return img


def main():
    """Example usage"""
    import sys

    if len(sys.argv) < 2:
        print(
            "Usage: python two_stage_detection.py <image_path> [tree_model] [defect_model]"
        )
        print("\nExample:")
        print("  python two_stage_detection.py image.jpg")
        print(
            "  python two_stage_detection.py image.jpg runs/detect/tree_detection_cpu/weights/best.pt runs/defects/tree_defects_detection/weights/best.pt"
        )
        sys.exit(1)

    image_path = sys.argv[1]

    # Default model paths
    tree_model = (
        sys.argv[2]
        if len(sys.argv) > 2
        else "runs/detect/tree_detection_cpu/weights/best.pt"
    )
    defect_model = (
        sys.argv[3]
        if len(sys.argv) > 3
        else "runs/defects/tree_defects_detection2/weights/best.pt"
    )

    # Check if models exist
    if not Path(tree_model).exists():
        print(f"Error: Tree model not found at {tree_model}")
        print("Please train the tree model first: python train_cpu.py")
        sys.exit(1)

    if not Path(defect_model).exists():
        print(f"Error: Defect model not found at {defect_model}")
        print("Please train the defect model first: python train_defects.py")
        sys.exit(1)

    # Check if image exists
    if not Path(image_path).exists():
        print(f"Error: Image not found at {image_path}")
        sys.exit(1)

    # Create detector
    detector = TwoStageDetector(tree_model, defect_model)

    # Run detection
    results = detector.detect(image_path, tree_conf=0.25, defect_conf=0.05)

    # Print results
    detector.print_results(results)

    # Save visualization
    output_path = f"detected_{Path(image_path).name}"
    detector.visualize(image_path, results, output_path)

    # Save JSON results
    json_path = f"results_{Path(image_path).stem}.json"
    with open(json_path, "w") as f:
        json.dump(results, f, indent=2)
    print(f"JSON results saved to: {json_path}")


if __name__ == "__main__":
    main()
