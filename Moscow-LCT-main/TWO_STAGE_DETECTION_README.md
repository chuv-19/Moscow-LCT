# Two-Stage Tree and Defect Detection System

## Overview

This system implements a sophisticated two-stage detection approach for tree health assessment:

1. **Stage 1**: Detect all trees in an image (using simple tree detection model)
2. **Stage 2**: Detect tree types and defects (using defect detection model with 22 classes)
3. **Stage 3**: Map each defect to its corresponding tree
4. **Stage 4**: Generate structured output with tree names and their defects

## Features

✅ **22-Class Detection Model**
- 11 tree types (ash, birch, bush, chestnut, larch, linden, maple, oak, pine, rowan, unknown_tree)
- 11 defect types (crack, dead_bush, deadtree, dry_crone, leaned_tree, markedtree, markettree, rot, stem_damage, stem_rot, tree_hole)

✅ **Two-Stage Architecture**
- First model finds all trees
- Second model identifies specific tree types and defects
- Smart mapping associates defects with trees using IoU and spatial analysis

✅ **Structured Output**
- Each tree gets a unique ID (Tree_1, Tree_2, etc.)
- Tree type identification
- List of all defects per tree
- Confidence scores for all detections

✅ **Multiple Interfaces**
- Command-line tool for batch processing
- Web interface with Streamlit
- Visualization with bounding boxes
- JSON export for integration

## Quick Start

### 1. Train the Defect Detection Model

```bash
python train_defects.py
```

This will:
- Train YOLOv11n on 288 images with 22 classes
- Train for 30 epochs (optimized for CPU)
- Save best model to `runs/defects/tree_defects_detection/weights/best.pt`

### 2. Run Detection on an Image

```bash
# Command line
python two_stage_detection.py path/to/image.jpg

# Or with custom models
python two_stage_detection.py image.jpg runs/detect/tree_detection_cpu/weights/best.pt runs/defects/tree_defects_detection/weights/best.pt
```

### 3. Launch Web Interface

```bash
python -m streamlit run two_stage_web.py
```

Then open: **http://localhost:8501**

## System Architecture

```
┌─────────────┐
│Input Image  │
└──────┬──────┘
       │
       ▼
┌──────────────────────────────────┐
│  Stage 1: Tree Detection         │
│  Model: tree_detection_cpu       │
│  Output: Tree bounding boxes     │
└──────────┬───────────────────────┘
           │
           ▼
┌──────────────────────────────────┐
│  Stage 2: Type & Defect Detection│
│  Model: tree_defects_detection   │
│  Output: 22-class detections     │
└──────────┬───────────────────────┘
           │
           ▼
┌──────────────────────────────────┐
│  Stage 3: Spatial Mapping        │
│  Match tree types to trees (IoU) │
│  Match defects to trees (spatial)│
└──────────┬───────────────────────┘
           │
           ▼
┌──────────────────────────────────┐
│  Stage 4: Structured Output      │
│  Tree ID + Type + Defect List    │
│  JSON export + Visualization     │
└──────────────────────────────────┘
```

## Output Format

### Console Output
```
============================================================
DETECTION RESULTS
============================================================
Image: sample_forest.jpg
Total Trees: 5
Total Defects: 3
============================================================

┌─ Tree_1
│  Type: oak
│  Confidence: 0.872
│  Type Confidence: 0.654
│  BBox: [120, 45, 340, 580]
│  Defects (2):
│    1. crack (conf: 0.543)
│    2. rot (conf: 0.421)
└──────────────────────────────────────────────────────────

┌─ Tree_2
│  Type: pine
│  Confidence: 0.765
│  Type Confidence: 0.712
│  BBox: [380, 60, 550, 620]
│  Defects: None ✓
└──────────────────────────────────────────────────────────

┌─ Tree_3
│  Type: maple
│  Confidence: 0.832
│  Type Confidence: 0.689
│  BBox: [600, 80, 780, 610]
│  Defects (1):
│    1. stem_damage (conf: 0.612)
└──────────────────────────────────────────────────────────
```

### JSON Output
```json
{
  "image": "/path/to/image.jpg",
  "total_trees": 3,
  "total_defects": 3,
  "trees": [
    {
      "id": "Tree_1",
      "type": "oak",
      "bbox": [120, 45, 340, 580],
      "confidence": 0.872,
      "type_confidence": 0.654,
      "defects": [
        {
          "type": "crack",
          "confidence": 0.543,
          "bbox": [145, 200, 180, 250]
        },
        {
          "type": "rot",
          "confidence": 0.421,
          "bbox": [200, 150, 250, 220]
        }
      ]
    },
    {
      "id": "Tree_2",
      "type": "pine",
      "bbox": [380, 60, 550, 620],
      "confidence": 0.765,
      "type_confidence": 0.712,
      "defects": []
    }
  ],
  "unmatched_defects": []
}
```

## Training Configuration

### Defect Model Training
```python
epochs=30                   # CPU-optimized
imgsz=640                   # Larger for defect details
batch=8                     # Memory efficient
split=0.8                   # 80% train, 20% validation
```

### Classes (22 Total)

**Tree Types (11)**:
1. ash
2. birch
3. bush
4. chestnut
5. larch
6. linden
7. maple
8. oak
9. pine
10. rowan
11. unknown_tree

**Defect Types (11)**:
1. crack - Cracks in trunk or branches
2. dead_bush - Dead shrubs/bushes
3. deadtree - Completely dead tree
4. dry_crone - Dry/dead crown
5. leaned_tree - Dangerously leaning tree
6. markedtree - Marked for removal/attention
7. markettree - Marked for market/logging
8. rot - Visible rot damage
9. stem_damage - Trunk/stem damage
10. stem_rot - Rot in the trunk/stem
11. tree_hole - Cavities or holes in tree

## Detection Logic

### Tree Type Mapping
- Uses IoU (Intersection over Union) between tree box and type detection
- Minimum IoU threshold: 0.3
- Best matching type is assigned to each tree

### Defect Mapping
- Checks if defect bounding box is inside or overlaps with tree box
- Uses both IoU and spatial center point analysis
- Minimum overlap threshold: 0.3
- One defect can map to multiple trees if overlapping

### Confidence Thresholds
- **Tree Detection**: 0.25 (default) - balanced sensitivity
- **Defect Detection**: 0.20 (default) - slightly more sensitive
- Both configurable via command line or web interface

## Usage Examples

### Example 1: Basic Detection
```bash
python two_stage_detection.py dataset/test/images/forest.jpg
```

### Example 2: Adjust Confidence
Modify in script or web interface:
```python
results = detector.detect(image_path, tree_conf=0.30, defect_conf=0.15)
```

### Example 3: Batch Processing
```bash
#!/bin/bash
for img in dataset/test/images/*.jpg; do
    python two_stage_detection.py "$img"
done
```

### Example 4: Web Interface
```bash
python -m streamlit run two_stage_web.py
```
Then:
1. Upload image
2. Adjust confidence sliders
3. Click "Run Detection"
4. View results with visualizations
5. Download annotated image or JSON

## File Structure

```
/Users/hanqnero/Dev/Roboflow model/
│
├── defects/                    # Defect dataset
│   └── dataset/
│       ├── data.yaml          # 22 classes config
│       └── train/
│           ├── images/        # 288 training images
│           └── labels/        # YOLO format annotations
│
├── runs/
│   ├── detect/                # Tree detection models
│   │   └── tree_detection_cpu/
│   │       └── weights/
│   │           └── best.pt    # Simple tree model
│   │
│   └── defects/               # Defect detection models
│       └── tree_defects_detection/
│           └── weights/
│               └── best.pt    # 22-class model
│
├── train_defects.py           # Training script for defects
├── two_stage_detection.py     # CLI detection tool
└── two_stage_web.py          # Web interface
```

## API Usage

### Python Integration
```python
from two_stage_detection import TwoStageDetector

# Initialize detector
detector = TwoStageDetector(
    tree_model_path='runs/detect/tree_detection_cpu/weights/best.pt',
    defect_model_path='runs/defects/tree_defects_detection/weights/best.pt'
)

# Run detection
results = detector.detect('image.jpg', tree_conf=0.25, defect_conf=0.20)

# Print results
detector.print_results(results)

# Create visualization
detector.visualize('image.jpg', results, 'output.jpg')

# Access structured data
for tree in results['trees']:
    print(f"{tree['id']}: {tree['type']}")
    for defect in tree['defects']:
        print(f"  - {defect['type']}")
```

## Performance Metrics

### Expected Training Results (30 epochs, CPU)
- Training time: ~2-3 hours on Apple M1
- mAP50: 0.40-0.60 (depends on dataset quality)
- Classes: 22 (more complex than simple tree detection)

### Inference Performance
- CPU (Apple M1): ~50-100ms per image per model
- Total time per image: ~150-250ms (both stages)
- Memory: ~1-2GB RAM

## Troubleshooting

### Model Not Found
```bash
# Check if models exist
ls runs/detect/tree_detection_cpu/weights/best.pt
ls runs/defects/tree_defects_detection/weights/best.pt

# Train if missing
python train_cpu.py              # Tree model
python train_defects.py          # Defect model
```

### Low Detection Accuracy
- Lower confidence thresholds (try 0.15-0.20)
- Train for more epochs (50-100)
- Increase image size (imgsz=800)
- Use larger model (yolo11s or yolo11m)

### Defects Not Mapping to Trees
- Check if trees are being detected in Stage 1
- Adjust IoU threshold in code (currently 0.3)
- Verify defects are actually within tree bounding boxes
- Lower tree confidence to detect more trees

### Training Issues
- Ensure dataset structure is correct
- Check data.yaml paths
- Verify labels exist for all images
- Monitor GPU/CPU memory usage

## Advanced Configuration

### Custom Confidence Thresholds
Edit `two_stage_detection.py`:
```python
# Line ~270
results = detector.detect(image_path, tree_conf=0.30, defect_conf=0.15)
```

### Custom IoU Threshold
Edit `two_stage_detection.py`:
```python
# In box_contains method, line ~57
def box_contains(self, outer_box, inner_box, threshold=0.2):  # Lower = more matches
```

### Training Adjustments
Edit `train_defects.py`:
```python
results = model.train(
    epochs=50,          # More epochs
    imgsz=800,          # Larger images
    batch=4,            # Smaller batch for more memory
    patience=15,        # More patience
)
```

## Integration Examples

### REST API Wrapper
```python
from flask import Flask, request, jsonify
from two_stage_detection import TwoStageDetector

app = Flask(__name__)
detector = TwoStageDetector('tree_model.pt', 'defect_model.pt')

@app.route('/detect', methods=['POST'])
def detect():
    file = request.files['image']
    results = detector.detect(file)
    return jsonify(results)
```

### Batch Processing Script
```python
from pathlib import Path
from two_stage_detection import TwoStageDetector
import json

detector = TwoStageDetector('tree_model.pt', 'defect_model.pt')
image_dir = Path('images_to_process')

all_results = []
for img_path in image_dir.glob('*.jpg'):
    results = detector.detect(str(img_path))
    all_results.append(results)
    
with open('batch_results.json', 'w') as f:
    json.dump(all_results, f, indent=2)
```

## Future Enhancements

- [ ] Add severity scoring for defects
- [ ] Implement health status classification per tree
- [ ] Add temporal tracking (compare images over time)
- [ ] Support for video stream processing
- [ ] Export to GIS formats (GeoJSON, Shapefile)
- [ ] Multi-language support for tree/defect names
- [ ] Mobile app integration
- [ ] Cloud deployment (AWS/GCP/Azure)

## Citation

Dataset: LCT Tree Defect Dataset
Model: YOLOv11 (Ultralytics)
License: MIT

## Support

For issues or questions:
1. Check documentation
2. Review training logs in `runs/defects/`
3. Test with known good images
4. Verify model files exist and are not corrupted

---

**System Status**: ✅ Ready for deployment
**Last Updated**: October 2, 2025