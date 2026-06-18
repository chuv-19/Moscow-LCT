#!/usr/bin/env python3
"""
Two-Stage Tree and Defect Detection Web GUI
Streamlit interface for detecting trees and their defects
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

# Page configuration
st.set_page_config(page_title="Tree & Defect Detection", page_icon="🌲", layout="wide")


@st.cache_resource
def load_detector(tree_model_path, defect_model_path):
    """Load detector with caching"""
    try:
        detector = TwoStageDetector(tree_model_path, defect_model_path)
        return detector, None
    except Exception as e:
        return None, str(e)


def find_models():
    """Find trained models"""
    tree_model = Path("runs/detect/tree_detection_cpu/weights/best.pt")
    defect_model = Path("runs/defects/tree_defects_detection2/weights/best.pt")

    return (
        str(tree_model) if tree_model.exists() else None,
        str(defect_model) if defect_model.exists() else None,
    )


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

    # Sidebar
    with st.sidebar:
        st.header("⚙️ Configuration")

        # Model status
        st.subheader("Models")
        tree_model, defect_model = find_models()

        if tree_model and defect_model:
            st.success("✅ Tree Model")
            st.success("✅ Defect Model")
            detector, error = load_detector(tree_model, defect_model)
            if error:
                st.error(f"Error loading models: {error}")
                detector = None
        else:
            if not tree_model:
                st.error("❌ Tree Model Not Found")
                st.info("Train with: `python train_cpu.py`")
            if not defect_model:
                st.error("❌ Defect Model Not Found")
                st.info("Train with: `python train_defects.py`")
            detector = None

        st.markdown("---")

        # Detection settings
        st.subheader("Detection Settings")
        tree_conf = st.slider("Tree Confidence", 0.05, 0.95, 0.25, 0.05)
        defect_conf = st.slider("Defect Confidence", 0.05, 0.95, 0.20, 0.05)

        st.markdown("---")

        # Info
        st.subheader("ℹ️ Detection Classes")
        with st.expander("Tree Types (2)"):
            st.markdown(
                """
            - Bush
            - Oak
            """
            )

        with st.expander("Defect Types (12)"):
            st.markdown(
                """
            - Crack, Dead Bush, Dead Tree
            - Dry Crown, Leaned Tree
            - Marked Tree, Market Tree
            - Marked Tree (variant)
            - Rot, Stem Damage
            - Stem Rot, Tree Hole
            """
            )

    # Main content
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
        type=["jpg", "jpeg", "png"],
        help="Select an image to detect trees and their defects",
    )

    if uploaded_file is not None:
        # Load image
        image = Image.open(uploaded_file)

        # Save temporarily
        with tempfile.NamedTemporaryFile(delete=False, suffix=".jpg") as tmp_file:
            image.save(tmp_file.name)
            tmp_path = tmp_file.name

        # Display original image
        col1, col2 = st.columns([1, 1])

        with col1:
            st.subheader("📷 Original Image")
            st.image(image, width=600)

        with col2:
            st.subheader("🎯 Detection Results")

            if st.button("🚀 Run Detection", type="primary", use_container_width=True):
                with st.spinner("Running two-stage detection..."):
                    try:
                        # Run detection
                        results = detector.detect(tmp_path, tree_conf, defect_conf)

                        # Create visualization
                        vis_img = detector.visualize(tmp_path, results)
                        vis_img_rgb = cv2.cvtColor(vis_img, cv2.COLOR_BGR2RGB)

                        # Display
                        st.image(vis_img_rgb, width=600)

                        # Save to session state
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

        # Cleanup
        try:
            Path(tmp_path).unlink()
        except:
            pass

    else:
        st.info("👆 Please upload an image to get started")


if __name__ == "__main__":
    main()
