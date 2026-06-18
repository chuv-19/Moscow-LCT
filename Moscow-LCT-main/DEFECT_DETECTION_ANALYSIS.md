# Defect Detection Model Analysis

## Current Status

The defect detection model has been successfully trained but shows **low accuracy**. Here's the analysis:

### Model Performance Metrics

- **Model**: YOLOv11n (nano)
- **Training Duration**: 30 epochs (~1 hour)
- **Final mAP50**: 0.079 (7.9%)
- **Final mAP50-95**: 0.066 (6.6%)

### Why Detection is Poor

#### 1. **Small Dataset for Too Many Classes**
- **Total Images**: 288
- **Total Classes**: 22 (11 tree types + 11 defects)
- **Average per class**: ~13 images
- **Industry Minimum**: 100-200 images per class for good performance
- **Recommended**: 500+ images per class for production quality

#### 2. **Class Distribution Issues**
Looking at the validation results, many classes have very low detection rates:
- `ash`: mAP50 = 0.00731 (0.7%)
- `chestnut`: mAP50 = 0.00 (0%)
- `crack`: mAP50 = 0.134 (13.4%)
- `larch`: mAP50 = 0.00 (0%)
- `markedtree`: mAP50 = 0.00 (0%)
- `rot`: mAP50 = 0.00 (0%)

Some classes perform better:
- `oak`: mAP50 = 0.39 (39%)
- `maple`: mAP50 = 0.239 (23.9%)
- `unknown_tree`: mAP50 = 0.378 (37.8%)

#### 3. **Confidence Threshold Impact**
- Default threshold of 0.20 filters out most detections
- Model is not confident enough due to insufficient training data
- Lowering to 0.05 allows more detections but may increase false positives

## Current Workaround

**The web interface now uses a default defect confidence of 0.05** instead of 0.20 to allow the model to detect more objects despite low confidence.

## Test Results

Testing on training image `_Vr0_6HYzc4_jpg.rf.76846c2fdfa93cdbd1e5c43a851d2e9f.jpg`:

```
Confidence 0.05: 3 detections
  - leaned_tree: 0.281
  - leaned_tree: 0.069
  - leaned_tree: 0.061

Confidence 0.10: 1 detection
Confidence 0.15: 1 detection
Confidence 0.20: 1 detection
Confidence 0.25: 1 detection
Confidence 0.30: 0 detections
```

## Recommendations to Improve Detection

### Short-term Fixes (No Re-training)

1. **Lower Confidence Threshold**
   - Use 0.05-0.10 for defect detection
   - Accept some false positives
   - Current web interface default: 0.05

2. **Focus on Better Classes**
   - Oak, Maple, Unknown_tree, Crack perform better
   - Filter results to only show high-confidence detections
   - Add confidence score to output

### Long-term Solutions (Requires Data Collection)

#### Option 1: Collect More Data
- **Target**: 200+ images per class
- **Total needed**: ~4,400 images (22 classes × 200)
- **Tools**: Roboflow, Label Studio, CVAT
- **Time estimate**: 2-4 weeks of labeling

#### Option 2: Reduce Number of Classes
Split into separate models:
- **Model 1**: Tree species only (11 classes)
- **Model 2**: Defects only (11 classes)
- **Model 3**: Healthy vs Unhealthy (2 classes)

This gives each model more data per class.

#### Option 3: Data Augmentation
Current training uses basic augmentation:
```python
hsv_h=0.015, hsv_s=0.7, hsv_v=0.4
translate=0.1, scale=0.5
fliplr=0.5, mosaic=1.0
```

Enhance with:
- More aggressive augmentation
- External data sources
- Synthetic data generation
- Transfer learning from similar datasets

#### Option 4: Use Pre-trained Weights
- Start from forestry/tree detection models
- Fine-tune on your specific defects
- Check Roboflow Universe for similar datasets

### Training Improvements

#### Retrain with Better Parameters:

```python
# Increase training time
epochs=100  # Current: 30

# Use larger model
model = YOLO("yolo11s.pt")  # or yolo11m.pt instead of yolo11n.pt

# Increase image size
imgsz=1280  # Current: 640

# Lower learning rate for fine-tuning
lr0=0.0001  # Current: 0.01

# Add more augmentation
mixup=0.15  # Current: 0.0
copy_paste=0.3  # New
```

#### Use Transfer Learning:

```python
# Start from a model trained on similar data
model = YOLO("path/to/forestry_model.pt")
model.train(
    data="defects/dataset/data.yaml",
    epochs=100,
    # ... other params
)
```

## What to Expect with Current Model

### ✅ Will Work:
- Tree detection (Stage 1) - works well
- High-confidence defect detection (>0.20)
- Tree type identification for common types (oak, maple, birch)
- Leaned trees (best performing defect class)

### ⚠️ May Not Work Well:
- Rare defect types (rot, crack, stem damage)
- Low-confidence detections (0.05-0.15)
- Small defects in images
- Rare tree types (ash, larch, chestnut)

### ❌ Will Not Work:
- Classes with 0% mAP (markedtree, rot for many images)
- Detecting defects smaller than training data
- Generalizing to very different image conditions

## Usage Guidelines

### For Best Results:

1. **Use Low Confidence Threshold** (0.05-0.10)
2. **Manually Verify Results** - Model is not production-ready
3. **Focus on Common Classes** - Oak, Maple, Birch, Leaned_tree
4. **Test on Similar Images** - Model trained on specific image types
5. **Consider it a Prototype** - Good for proof-of-concept, not production

### In the Web Interface:

- Default tree confidence: **0.25** (good)
- Default defect confidence: **0.05** (allows more detections)
- Adjust sliders to find best balance for your images
- Download JSON results to analyze confidence scores

## Next Steps

### Immediate Actions:
1. ✅ Lower default confidence to 0.05 (DONE)
2. ✅ Add warning about low model accuracy (DONE)
3. Test on various images to understand model behavior
4. Document which classes work best

### Future Improvements:
1. **Collect more data** (highest priority)
2. **Retrain with larger model** (yolo11s or yolo11m)
3. **Increase training epochs** (100+)
4. **Split into separate models** if possible
5. **Consider cloud-based training** with GPU for faster iteration

## Summary

The current model **works but has low accuracy** due to insufficient training data. It can detect some defects but should be considered a **proof-of-concept** rather than a production system. 

**Key Takeaway**: Need 10-20x more training data (2,000-4,000 images) for production-quality results.

For now, use confidence threshold of **0.05** and manually verify all results.
