#!/usr/bin/env python3
"""
YOLOv11 Two-Stage Tree & Defect Detection Web GUI
Web-based GUI using Streamlit for detecting trees and their defects
"""

import streamlit as st
from PIL import Image
import cv2
import numpy as np
from pathlib import Path
import tempfile
import json
import torch

# Fix for PyTorch 2.6+ weights_only security change
try:
    from ultralytics.nn.tasks import DetectionModel

    torch.serialization.add_safe_globals([DetectionModel])
except Exception:
    pass  # Older PyTorch versions don't have this

from two_stage_detection import TwoStageDetector
from config_loader import load_config

# Page configuration
st.set_page_config(page_title="Tree & Defect Detection", page_icon="🌲", layout="wide")

# Load configuration
config = load_config()


# Cache the model loading
@st.cache_resource
def load_detector(tree_model_path, defect_model_path):
    """Load two-stage detector with caching"""
    try:
        detector = TwoStageDetector(tree_model_path, defect_model_path)
        return detector, None
    except Exception as e:
        return None, str(e)


def find_models():
    """Find both trained models using config"""
    tree_model = config.get_model_path()

    # Get defect model path from config
    config_dict = config.config
    if (
        config_dict
        and "model" in config_dict
        and "defect_model_path" in config_dict["model"]
    ):
        defect_model_path = config_dict["model"]["defect_model_path"]
        defect_model = Path(config.get_project_root()) / defect_model_path
        if defect_model.exists():
            return tree_model, str(defect_model)

    # Fallback to default path
    defect_model = Path("runs/defects/tree_defects_detection2/weights/best.pt")
    return tree_model, str(defect_model) if defect_model.exists() else None


def run_inference(detector, image, tree_conf_threshold, defect_conf_threshold):
    """Run two-stage inference on image"""
    # Save uploaded image temporarily
    with tempfile.NamedTemporaryFile(delete=False, suffix=".jpg") as tmp_file:
        image.save(tmp_file.name)
        tmp_path = tmp_file.name

    # Run two-stage detection
    results = detector.detect(tmp_path, tree_conf_threshold, defect_conf_threshold)

    # Create visualization
    vis_img = detector.visualize(tmp_path, results)
    vis_img_rgb = cv2.cvtColor(vis_img, cv2.COLOR_BGR2RGB)

    # Cleanup
    Path(tmp_path).unlink()

    return results, vis_img_rgb


def format_results_html(results):
    """Format results as HTML for better display"""
    html = "<div style='font-family: monospace;'>"

    for tree in results["trees"]:
        # Tree header
        tree_color = "#2ecc71" if not tree["defects"] else "#e74c3c"
        html += f"<div style='margin-bottom: 20px; padding: 15px; border-left: 4px solid {tree_color}; background-color: #f8f9fa;'>"
        html += (
            f"<h4 style='margin: 0 0 10px 0; color: {tree_color};'>🌲 {tree['id']}</h4>"
        )
        html += f"<p style='margin: 5px 0;'><b>Type:</b> {tree['type']}</p>"
        html += (
            f"<p style='margin: 5px 0;'><b>Confidence:</b> {tree['confidence']:.1%}</p>"
        )

        if "type_confidence" in tree:
            html += f"<p style='margin: 5px 0;'><b>Type Confidence:</b> {tree['type_confidence']:.1%}</p>"

        if tree["defects"]:
            html += f"<p style='margin: 10px 0 5px 0;'><b>⚠️ Defects ({len(tree['defects'])}):</b></p>"
            html += "<ul style='margin: 0; padding-left: 20px;'>"
            for defect in tree["defects"]:
                html += f"<li>{defect['type']} (confidence: {defect['confidence']:.1%})</li>"
            html += "</ul>"
        else:
            html += "<p style='margin: 10px 0 0 0; color: #27ae60;'>✓ No defects detected</p>"

        html += "</div>"

    if results["unmatched_defects"]:
        html += "<div style='margin-top: 20px; padding: 15px; border-left: 4px solid #f39c12; background-color: #fef5e7;'>"
        html += f"<h4 style='margin: 0 0 10px 0; color: #f39c12;'>⚠️ Unmatched Defects ({len(results['unmatched_defects'])})</h4>"
        html += "<ul style='margin: 0; padding-left: 20px;'>"
        for defect in results["unmatched_defects"]:
            html += (
                f"<li>{defect['class']} (confidence: {defect['confidence']:.1%})</li>"
            )
        html += "</ul>"
        html += "</div>"

    html += "</div>"
    return html


def main():
    # Title
    st.title("🌲 Tree & Defect Detection System")
    st.markdown(
        "Two-stage detection: First detects trees, then identifies defects within each tree"
    )
    st.markdown("---")

    # Sidebar for controls
    with st.sidebar:
        st.header("⚙️ Configuration")

        # Model selection
        st.subheader("Models")
        tree_model_path, defect_model_path = find_models()

        detector = None
        if tree_model_path and defect_model_path:
            # Show model status
            st.success("✅ Tree Model")
            st.success("✅ Defect Model")

            detector, error = load_detector(tree_model_path, defect_model_path)
            if error:
                st.error(f"Error loading models: {error}")
                detector = None
        else:
            if not tree_model_path:
                st.error("❌ Tree Model Not Found")
                st.info("Train with: `python train_cpu.py`")
            if not defect_model_path:
                st.error("❌ Defect Model Not Found")
                st.info("Train with: `python train_defects.py`")
            detector = None

        st.markdown("---")

        # Get inference settings from config
        inference_settings = config.get_inference_settings()

        # Confidence thresholds
        st.subheader("Detection Settings")
        tree_conf = st.slider(
            "Tree Confidence",
            min_value=inference_settings["min_confidence"],
            max_value=inference_settings["max_confidence"],
            value=inference_settings["default_confidence"],
            step=inference_settings["confidence_step"],
            help="Confidence threshold for tree detection",
        )

        defect_conf = st.slider(
            "Defect Confidence",
            min_value=inference_settings["min_confidence"],
            max_value=inference_settings["max_confidence"],
            value=0.05,  # Lower default for defect model with low mAP
            step=inference_settings["confidence_step"],
            help="Confidence threshold for defect detection (model has low mAP, use lower threshold)",
        )

        st.markdown("---")

        # Info
        st.subheader("ℹ️ Detection Classes")
        with st.expander("Tree Types (11)"):
            st.markdown(
                """
            - Ash, Birch, Bush, Chestnut
            - Larch, Linden, Maple
            - Oak, Pine, Rowan
            - Unknown Tree
            """
            )

        with st.expander("Defect Types (11)"):
            st.markdown(
                """
            - Crack, Dead Bush, Dead Tree
            - Dry Crown, Leaned Tree
            - Marked Tree, Market Tree
            - Rot, Stem Damage
            - Stem Rot, Tree Hole
            """
            )

    # Main content area
    if detector is None:
        st.error("❌ Models not available. Please train both models first.")

        col1, col2 = st.columns(2)
        with col1:
            st.code("python train_cpu.py", language="bash")
            st.caption("Train tree detection model")
        with col2:
            st.code("python train_defects.py", language="bash")
            st.caption("Train defect detection model")
        return

    # File uploader
    st.header("📁 Upload Image")
    uploaded_file = st.file_uploader(
        "Choose an image file",
        type=["jpg", "jpeg", "png", "bmp", "gif", "tiff"],
        help="Select an image to detect trees",
    )

    if uploaded_file is not None:
        # Load image
        image = Image.open(uploaded_file)

        # Create two columns for display
        col1, col2 = st.columns(2)

        with col1:
            st.subheader("📷 Original Image")
            st.image(image, use_container_width=True)

        with col2:
            st.subheader("🎯 Detection Results")

            # Run inference button
            if st.button("🚀 Run Detection", type="primary", use_container_width=True):
                with st.spinner("Running two-stage detection..."):
                    try:
                        results, vis_img = run_inference(
                            detector, image, tree_conf, defect_conf
                        )

                        # Display result image
                        st.image(vis_img, use_container_width=True)

                        # Store in session state
                        st.session_state["results"] = results
                        st.session_state["vis_img"] = vis_img

                    except Exception as e:
                        st.error(f"Error during detection: {str(e)}")

        # Show results if available
        if "results" in st.session_state:
            results = st.session_state["results"]

            st.markdown("---")
            st.subheader("📊 Detection Summary")

            # Summary metrics
            col_a, col_b, col_c, col_d = st.columns(4)

            with col_a:
                st.metric("Total Trees", results["total_trees"])

            with col_b:
                st.metric("Total Defects", results["total_defects"])

            with col_c:
                healthy_trees = sum(1 for t in results["trees"] if not t["defects"])
                st.metric("Healthy Trees", healthy_trees)

            with col_d:
                unhealthy_trees = results["total_trees"] - healthy_trees
                st.metric("Trees with Defects", unhealthy_trees)

            # Debug info
            if results["total_defects"] == 0 and results["total_trees"] > 0:
                st.warning(
                    "⚠️ No defects detected. The defect model has low accuracy (mAP50: 7.9%). Try lowering the defect confidence threshold to 0.05 or checking if the image has visible defects."
                )

            # Detailed results
            st.markdown("---")
            st.subheader("📋 Detailed Results")

            # Display formatted results
            html_results = format_results_html(results)
            st.markdown(html_results, unsafe_allow_html=True)

            # Download options
            st.markdown("---")
            st.subheader("💾 Download Results")

            col_dl1, col_dl2 = st.columns(2)

            with col_dl1:
                # Download image
                if "vis_img" in st.session_state:
                    vis_img = st.session_state["vis_img"]
                    is_success, buffer = cv2.imencode(".jpg", vis_img)
                    if is_success:
                        st.download_button(
                            label="Download Annotated Image",
                            data=buffer.tobytes(),
                            file_name=f"detected_{uploaded_file.name}",
                            mime="image/jpeg",
                            use_container_width=True,
                        )

            with col_dl2:
                # Download JSON
                json_str = json.dumps(results, indent=2)
                st.download_button(
                    label="Download JSON Results",
                    data=json_str,
                    file_name=f"results_{Path(uploaded_file.name).stem}.json",
                    mime="application/json",
                    use_container_width=True,
                )
    else:
        # Instructions when no image is uploaded
        st.info("👆 Please upload an image to get started")

        # Example images
        st.subheader("💡 Try with test images")
        test_dir = config.get_test_images_dir()
        display_settings = config.get_display_settings()

        if test_dir and test_dir.exists():
            test_images = list(test_dir.glob("*.jpg"))[
                : display_settings["max_example_images"]
            ]

            if test_images:
                st.markdown("Example images from your test dataset:")
                cols = st.columns(len(test_images))

                for idx, img_path in enumerate(test_images):
                    with cols[idx]:
                        try:
                            img = Image.open(img_path)
                            st.image(
                                img, caption=img_path.name, use_container_width=True
                            )
                        except:
                            pass
        else:
            st.info("Test images directory not found. Check config.ini")


if __name__ == "__main__":
    main()
