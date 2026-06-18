# Updated Defect Detection Classes

## Overview
The defect detection dataset has been updated to include **14 classes** (down from the previous 22 classes).

## Training Status
- **Training Script**: `train_defects.py` 
- **Epochs**: 40 (updated from 30)
- **Model**: YOLOv11n
- **Status**: Training in progress

## Class Breakdown

### Tree Types (2 classes)
1. `bush` - Bush/shrub vegetation
2. `oak` - Oak trees

### Defect Types (12 classes)
1. `crack` - Cracks in trees
2. `dead_bush` - Dead bushes
3. `deadtree` - Dead trees
4. `dry_crone` - Dry crown/top
5. `leaned_tree` - Leaning trees
6. `marked_tree` - Marked trees (variant 1)
7. `markedtree` - Marked trees (variant 2)
8. `markettree` - Market trees
9. `rot` - Rot/decay
10. `stem_damage` - Stem damage
11. `stem_rot` - Stem rot
12. `tree_hole` - Holes in trees

## System Updates

### Updated Files
1. **`train_defects.py`**
   - Updated to train for 40 epochs
   - Updated class count from 22 to 14
   - Corrected class descriptions in comments

2. **`two_stage_detection.py`**
   - Updated `tree_classes` set to include only: `bush`, `oak`
   - Updated `defect_classes` set to include all 12 defect types
   - Added `marked_tree` variant to defect classes

3. **`two_stage_web.py`**
   - Updated sidebar info to show 2 tree types
   - Updated sidebar info to show 12 defect types
   - Corrected class listings in expandable sections

## How to Use

### 1. Wait for Training to Complete
The model is currently training for 40 epochs. Monitor progress in the terminal.

### 2. Run Two-Stage Detection
After training completes, use the updated two-stage detection system:

```bash
# Command-line interface
python two_stage_detection.py <image_path>

# Web interface
streamlit run two_stage_web.py
```

### 3. Expected Output
- **Stage 1**: Detects trees using the simple tree detection model
- **Stage 2**: Identifies tree types (bush/oak) and defects using the updated defect model
- **Stage 3**: Maps tree types to detected trees
- **Stage 4**: Associates defects with their corresponding trees

## Model Location
Once training completes, the model will be saved at:
```
runs/defects/tree_defects_detection/weights/best.pt
```

## Notes
- The system now focuses on bush and oak detection for tree typing
- Defect detection covers 12 different types of tree problems
- Lower confidence thresholds may be needed for defect detection (default: 0.05)
- The two-stage system maintains backward compatibility with existing tree detection models

## Configuration
Dataset configuration: `defects/dataset/data.yaml`
```yaml
nc: 14
names: ['bush', 'crack', 'dead_bush', 'deadtree', 'dry_crone', 'leaned_tree', 
        'marked_tree', 'markedtree', 'markettree', 'oak', 'rot', 
        'stem_damage', 'stem_rot', 'tree_hole']
```
