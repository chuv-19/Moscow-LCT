#!/usr/bin/env python3
"""
Tree & Defect Detection - Desktop Application
Windows GUI application with full two-stage detection capabilities
"""

import tkinter as tk
from tkinter import ttk, filedialog, messagebox, scrolledtext
from PIL import Image, ImageTk
import cv2
import numpy as np
from pathlib import Path
import json
from datetime import datetime
import threading
import torch

# Fix for PyTorch 2.6+ weights_only security change
try:
    from ultralytics.nn.tasks import DetectionModel

    torch.serialization.add_safe_globals([DetectionModel])
except Exception:
    pass  # Older PyTorch versions don't have this

from two_stage_detection import TwoStageDetector


class TreeDetectionApp:
    """Desktop GUI Application for Tree & Defect Detection"""

    def __init__(self, root):
        self.root = root
        self.root.title("🌲 Tree & Defect Detection System")
        self.root.geometry("1400x900")
        self.root.minsize(1200, 800)

        # Variables
        self.detector = None
        self.original_image = None
        self.detected_image = None
        self.results = None
        self.image_path = None

        # Get script directory for relative paths
        self.script_dir = Path(__file__).parent.resolve()

        # Initialize UI
        self.setup_ui()
        self.load_models()

    def setup_ui(self):
        """Setup the user interface"""
        # Main container
        main_container = ttk.Frame(self.root, padding="10")
        main_container.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_container.columnconfigure(1, weight=1)
        main_container.rowconfigure(1, weight=1)

        # Title
        title_frame = ttk.Frame(main_container)
        title_frame.grid(
            row=0, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 10)
        )

        title_label = ttk.Label(
            title_frame,
            text="🌲 Tree & Defect Detection System",
            font=("Arial", 20, "bold"),
        )
        title_label.pack()

        subtitle_label = ttk.Label(
            title_frame,
            text="Two-Stage Detection: Trees + Defects",
            font=("Arial", 10),
        )
        subtitle_label.pack()

        # Left Panel - Controls
        self.setup_left_panel(main_container)

        # Right Panel - Images and Results
        self.setup_right_panel(main_container)

        # Status Bar
        self.status_bar = ttk.Label(
            self.root, text="Ready", relief=tk.SUNKEN, anchor=tk.W
        )
        self.status_bar.grid(row=1, column=0, sticky=(tk.W, tk.E))

    def setup_left_panel(self, parent):
        """Setup left control panel"""
        left_panel = ttk.Frame(parent, padding="5")
        left_panel.grid(row=1, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), padx=(0, 5))

        # Model Status
        model_frame = ttk.LabelFrame(left_panel, text="Model Status", padding="10")
        model_frame.pack(fill=tk.X, pady=(0, 10))

        self.tree_model_status = ttk.Label(
            model_frame, text="Tree Model: Loading...", foreground="orange"
        )
        self.tree_model_status.pack(anchor=tk.W)

        self.defect_model_status = ttk.Label(
            model_frame, text="Defect Model: Loading...", foreground="orange"
        )
        self.defect_model_status.pack(anchor=tk.W)

        # Image Controls
        image_frame = ttk.LabelFrame(left_panel, text="Image Selection", padding="10")
        image_frame.pack(fill=tk.X, pady=(0, 10))

        self.select_image_btn = ttk.Button(
            image_frame, text="📁 Select Image", command=self.select_image, width=25
        )
        self.select_image_btn.pack(fill=tk.X, pady=2)

        self.image_path_label = ttk.Label(
            image_frame, text="No image selected", foreground="gray", wraplength=250
        )
        self.image_path_label.pack(anchor=tk.W, pady=(5, 0))

        # Detection Settings
        settings_frame = ttk.LabelFrame(
            left_panel, text="Detection Settings", padding="10"
        )
        settings_frame.pack(fill=tk.X, pady=(0, 10))

        # Tree Confidence
        ttk.Label(settings_frame, text="Tree Confidence:").pack(anchor=tk.W)
        self.tree_conf = tk.DoubleVar(value=0.25)
        tree_conf_scale = ttk.Scale(
            settings_frame,
            from_=0.05,
            to=0.95,
            orient=tk.HORIZONTAL,
            variable=self.tree_conf,
            command=self.update_tree_conf_label,
        )
        tree_conf_scale.pack(fill=tk.X)
        self.tree_conf_label = ttk.Label(settings_frame, text="0.25")
        self.tree_conf_label.pack(anchor=tk.W)

        ttk.Separator(settings_frame, orient=tk.HORIZONTAL).pack(fill=tk.X, pady=10)

        # Defect Confidence
        ttk.Label(settings_frame, text="Defect Confidence:").pack(anchor=tk.W)
        self.defect_conf = tk.DoubleVar(value=0.20)
        defect_conf_scale = ttk.Scale(
            settings_frame,
            from_=0.05,
            to=0.95,
            orient=tk.HORIZONTAL,
            variable=self.defect_conf,
            command=self.update_defect_conf_label,
        )
        defect_conf_scale.pack(fill=tk.X)
        self.defect_conf_label = ttk.Label(settings_frame, text="0.20")
        self.defect_conf_label.pack(anchor=tk.W)

        # Detection Button
        self.detect_btn = ttk.Button(
            left_panel,
            text="🚀 Run Detection",
            command=self.run_detection,
            state=tk.DISABLED,
        )
        self.detect_btn.pack(fill=tk.X, pady=10)

        # Progress
        self.progress = ttk.Progressbar(left_panel, mode="indeterminate")
        self.progress.pack(fill=tk.X, pady=(0, 10))

        # Export Options
        export_frame = ttk.LabelFrame(left_panel, text="Export Results", padding="10")
        export_frame.pack(fill=tk.X, pady=(0, 10))

        self.save_image_btn = ttk.Button(
            export_frame,
            text="💾 Save Annotated Image",
            command=self.save_image,
            state=tk.DISABLED,
        )
        self.save_image_btn.pack(fill=tk.X, pady=2)

        self.save_json_btn = ttk.Button(
            export_frame,
            text="📄 Save JSON Results",
            command=self.save_json,
            state=tk.DISABLED,
        )
        self.save_json_btn.pack(fill=tk.X, pady=2)

        # Class Information
        info_frame = ttk.LabelFrame(left_panel, text="Detection Classes", padding="10")
        info_frame.pack(fill=tk.BOTH, expand=True)

        info_text = scrolledtext.ScrolledText(
            info_frame, height=10, wrap=tk.WORD, font=("Arial", 9)
        )
        info_text.pack(fill=tk.BOTH, expand=True)
        info_text.insert(
            "1.0",
            "Tree Types (2):\n"
            "• Bush\n"
            "• Oak\n\n"
            "Defect Types (12):\n"
            "• Crack\n"
            "• Dead Bush\n"
            "• Dead Tree\n"
            "• Dry Crown\n"
            "• Leaned Tree\n"
            "• Marked Tree\n"
            "• Market Tree\n"
            "• Rot\n"
            "• Stem Damage\n"
            "• Stem Rot\n"
            "• Tree Hole",
        )
        info_text.config(state=tk.DISABLED)

    def setup_right_panel(self, parent):
        """Setup right panel for images and results"""
        right_panel = ttk.Frame(parent, padding="5")
        right_panel.grid(row=1, column=1, sticky=(tk.W, tk.E, tk.N, tk.S))
        right_panel.rowconfigure(0, weight=1)
        right_panel.rowconfigure(1, weight=0)
        right_panel.columnconfigure(0, weight=1)
        right_panel.columnconfigure(1, weight=1)

        # Image Display Area
        image_container = ttk.Frame(right_panel)
        image_container.grid(
            row=0, column=0, columnspan=2, sticky=(tk.W, tk.E, tk.N, tk.S)
        )

        # Original Image
        original_frame = ttk.LabelFrame(
            image_container, text="Original Image", padding="5"
        )
        original_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 5))

        self.original_canvas = tk.Canvas(original_frame, bg="gray90")
        self.original_canvas.pack(fill=tk.BOTH, expand=True)
        self.original_canvas_text = self.original_canvas.create_text(
            200, 150, text="No image loaded", fill="gray", font=("Arial", 12)
        )

        # Detected Image
        detected_frame = ttk.LabelFrame(
            image_container, text="Detection Results", padding="5"
        )
        detected_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self.detected_canvas = tk.Canvas(detected_frame, bg="gray90")
        self.detected_canvas.pack(fill=tk.BOTH, expand=True)
        self.detected_canvas_text = self.detected_canvas.create_text(
            200,
            150,
            text="Run detection to see results",
            fill="gray",
            font=("Arial", 12),
        )

        # Results Display
        results_frame = ttk.LabelFrame(
            right_panel, text="Detection Summary", padding="10"
        )
        results_frame.grid(
            row=1, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(10, 0)
        )

        self.results_text = scrolledtext.ScrolledText(
            results_frame, height=12, wrap=tk.WORD, font=("Courier", 9)
        )
        self.results_text.pack(fill=tk.BOTH, expand=True)

    def update_tree_conf_label(self, value):
        """Update tree confidence label"""
        self.tree_conf_label.config(text=f"{float(value):.2f}")

    def update_defect_conf_label(self, value):
        """Update defect confidence label"""
        self.defect_conf_label.config(text=f"{float(value):.2f}")

    def load_models(self):
        """Load detection models"""
        self.update_status("Loading models...")

        def load_in_thread():
            try:
                tree_model = (
                    self.script_dir
                    / "runs"
                    / "detect"
                    / "tree_detection_cpu"
                    / "weights"
                    / "best.pt"
                )
                defect_model = (
                    self.script_dir
                    / "runs"
                    / "defects"
                    / "tree_defects_detection2"
                    / "weights"
                    / "best.pt"
                )
                defect_model_alt = (
                    self.script_dir
                    / "runs"
                    / "defects"
                    / "tree_defects_detection"
                    / "weights"
                    / "best.pt"
                )

                # Use alternative if primary doesn't exist
                if not defect_model.exists() and defect_model_alt.exists():
                    defect_model = defect_model_alt

                if tree_model.exists() and defect_model.exists():
                    self.detector = TwoStageDetector(str(tree_model), str(defect_model))
                    self.root.after(0, self.on_models_loaded, True, True)
                else:
                    self.root.after(
                        0,
                        self.on_models_loaded,
                        tree_model.exists(),
                        defect_model.exists(),
                    )
            except Exception as e:
                self.root.after(0, self.on_models_error, str(e))

        thread = threading.Thread(target=load_in_thread, daemon=True)
        thread.start()

    def on_models_loaded(self, tree_ok, defect_ok):
        """Called when models are loaded"""
        if tree_ok:
            self.tree_model_status.config(
                text="✅ Tree Model: Ready", foreground="green"
            )
        else:
            self.tree_model_status.config(
                text="❌ Tree Model: Not Found", foreground="red"
            )

        if defect_ok:
            self.defect_model_status.config(
                text="✅ Defect Model: Ready", foreground="green"
            )
        else:
            self.defect_model_status.config(
                text="❌ Defect Model: Not Found", foreground="red"
            )

        if tree_ok and defect_ok:
            self.update_status("Models loaded successfully")
        else:
            self.update_status("Some models are missing. Train models first.")
            messagebox.showwarning(
                "Models Missing",
                "Some models are not found.\n\n"
                "Train models using:\n"
                "• python train_cpu.py (tree model)\n"
                "• python train_defects.py (defect model)",
            )

    def on_models_error(self, error):
        """Called when model loading fails"""
        self.tree_model_status.config(text="❌ Error Loading", foreground="red")
        self.defect_model_status.config(text="❌ Error Loading", foreground="red")
        self.update_status(f"Error: {error}")
        messagebox.showerror("Model Error", f"Failed to load models:\n{error}")

    def select_image(self):
        """Select an image file"""
        filename = filedialog.askopenfilename(
            title="Select Image",
            filetypes=[
                ("Image Files", "*.jpg *.jpeg *.png *.bmp"),
                ("JPEG", "*.jpg *.jpeg"),
                ("PNG", "*.png"),
                ("All Files", "*.*"),
            ],
        )

        if filename:
            self.image_path = filename
            self.load_image(filename)
            self.image_path_label.config(text=Path(filename).name, foreground="black")
            self.detect_btn.config(state=tk.NORMAL if self.detector else tk.DISABLED)
            self.update_status(f"Loaded: {Path(filename).name}")

    def load_image(self, path):
        """Load and display image"""
        try:
            # Load original image
            image = Image.open(path)
            self.original_image = image

            # Display original
            self.display_image(image, self.original_canvas)

            # Clear detected canvas
            self.detected_canvas.delete("all")
            self.detected_canvas_text = self.detected_canvas.create_text(
                200,
                150,
                text="Run detection to see results",
                fill="gray",
                font=("Arial", 12),
            )

            # Clear results
            self.results_text.delete("1.0", tk.END)
            self.detected_image = None
            self.results = None
            self.save_image_btn.config(state=tk.DISABLED)
            self.save_json_btn.config(state=tk.DISABLED)

        except Exception as e:
            messagebox.showerror("Image Error", f"Failed to load image:\n{e}")

    def display_image(self, image, canvas):
        """Display image on canvas with proper scaling"""
        canvas.delete("all")

        # Get canvas size
        canvas.update()
        canvas_width = canvas.winfo_width()
        canvas_height = canvas.winfo_height()

        if canvas_width <= 1 or canvas_height <= 1:
            canvas_width = 400
            canvas_height = 400

        # Calculate scaling
        img_width, img_height = image.size
        scale_w = canvas_width / img_width
        scale_h = canvas_height / img_height
        scale = min(scale_w, scale_h, 1.0)  # Don't upscale

        new_width = int(img_width * scale)
        new_height = int(img_height * scale)

        # Resize image
        resized = image.resize((new_width, new_height), Image.Resampling.LANCZOS)

        # Convert to PhotoImage
        photo = ImageTk.PhotoImage(resized)

        # Center image on canvas
        x = (canvas_width - new_width) // 2
        y = (canvas_height - new_height) // 2

        canvas.create_image(x, y, anchor=tk.NW, image=photo)
        canvas.image = photo  # Keep a reference

    def run_detection(self):
        """Run two-stage detection"""
        if not self.detector:
            messagebox.showerror("Error", "Models not loaded")
            return

        if not self.image_path:
            messagebox.showerror("Error", "No image selected")
            return

        self.detect_btn.config(state=tk.DISABLED)
        self.progress.start()
        self.update_status("Running detection...")

        def detect_in_thread():
            try:
                # Run detection
                results = self.detector.detect(
                    self.image_path,
                    tree_conf=self.tree_conf.get(),
                    defect_conf=self.defect_conf.get(),
                )

                # Create visualization
                vis_img = self.detector.visualize(self.image_path, results)

                self.root.after(0, self.on_detection_complete, results, vis_img)

            except Exception as e:
                self.root.after(0, self.on_detection_error, str(e))

        thread = threading.Thread(target=detect_in_thread, daemon=True)
        thread.start()

    def on_detection_complete(self, results, vis_img):
        """Called when detection is complete"""
        self.progress.stop()
        self.detect_btn.config(state=tk.NORMAL)

        # Store results
        self.results = results
        self.detected_image = vis_img

        # Convert BGR to RGB for display
        vis_img_rgb = cv2.cvtColor(vis_img, cv2.COLOR_BGR2RGB)
        pil_img = Image.fromarray(vis_img_rgb)

        # Display detected image
        self.display_image(pil_img, self.detected_canvas)

        # Display results
        self.display_results(results)

        # Enable export buttons
        self.save_image_btn.config(state=tk.NORMAL)
        self.save_json_btn.config(state=tk.NORMAL)

        self.update_status(
            f"Detection complete: {results['total_trees']} trees, {results['total_defects']} defects"
        )

    def on_detection_error(self, error):
        """Called when detection fails"""
        self.progress.stop()
        self.detect_btn.config(state=tk.NORMAL)
        self.update_status(f"Detection failed: {error}")
        messagebox.showerror("Detection Error", f"Detection failed:\n{error}")

    def display_results(self, results):
        """Display detection results"""
        self.results_text.delete("1.0", tk.END)

        # Summary
        self.results_text.insert(tk.END, "=" * 60 + "\n")
        self.results_text.insert(tk.END, "DETECTION RESULTS\n")
        self.results_text.insert(tk.END, "=" * 60 + "\n\n")
        self.results_text.insert(tk.END, f"Total Trees: {results['total_trees']}\n")
        self.results_text.insert(tk.END, f"Total Defects: {results['total_defects']}\n")

        healthy = sum(1 for t in results["trees"] if not t["defects"])
        unhealthy = results["total_trees"] - healthy
        self.results_text.insert(tk.END, f"Healthy Trees: {healthy}\n")
        self.results_text.insert(tk.END, f"Trees with Defects: {unhealthy}\n")
        self.results_text.insert(tk.END, "=" * 60 + "\n\n")

        # Tree details
        if not results["trees"]:
            self.results_text.insert(tk.END, "No trees detected.\n")
            return

        for tree in results["trees"]:
            self.results_text.insert(tk.END, f"┌─ {tree['id']}\n")
            self.results_text.insert(tk.END, f"│  Type: {tree['type']}\n")
            self.results_text.insert(
                tk.END, f"│  Confidence: {tree['confidence']:.3f}\n"
            )

            if "type_confidence" in tree:
                self.results_text.insert(
                    tk.END, f"│  Type Confidence: {tree['type_confidence']:.3f}\n"
                )

            if tree["defects"]:
                self.results_text.insert(
                    tk.END, f"│  Defects ({len(tree['defects'])}):\n"
                )
                for i, defect in enumerate(tree["defects"], 1):
                    self.results_text.insert(
                        tk.END,
                        f"│    {i}. {defect['type']} (conf: {defect['confidence']:.3f})\n",
                    )
            else:
                self.results_text.insert(tk.END, "│  Defects: None ✓\n")

            self.results_text.insert(tk.END, f"└{'─' * 58}\n\n")

        if results["unmatched_defects"]:
            self.results_text.insert(
                tk.END,
                f"\n⚠ Unmatched Defects ({len(results['unmatched_defects'])}):\n",
            )
            for defect in results["unmatched_defects"]:
                self.results_text.insert(
                    tk.END,
                    f"  - {defect['class']} (conf: {defect['confidence']:.3f})\n",
                )

    def save_image(self):
        """Save annotated image"""
        if self.detected_image is None:
            return

        filename = filedialog.asksaveasfilename(
            title="Save Annotated Image",
            defaultextension=".jpg",
            filetypes=[("JPEG", "*.jpg"), ("PNG", "*.png"), ("All Files", "*.*")],
            initialfile=f"detected_{Path(self.image_path).stem}.jpg",
        )

        if filename:
            try:
                cv2.imwrite(filename, self.detected_image)
                self.update_status(f"Saved: {Path(filename).name}")
                messagebox.showinfo("Success", f"Image saved:\n{filename}")
            except Exception as e:
                messagebox.showerror("Save Error", f"Failed to save image:\n{e}")

    def save_json(self):
        """Save results as JSON"""
        if self.results is None:
            return

        filename = filedialog.asksaveasfilename(
            title="Save JSON Results",
            defaultextension=".json",
            filetypes=[("JSON", "*.json"), ("All Files", "*.*")],
            initialfile=f"results_{Path(self.image_path).stem}.json",
        )

        if filename:
            try:
                with open(filename, "w") as f:
                    json.dump(self.results, f, indent=2)
                self.update_status(f"Saved: {Path(filename).name}")
                messagebox.showinfo("Success", f"Results saved:\n{filename}")
            except Exception as e:
                messagebox.showerror("Save Error", f"Failed to save JSON:\n{e}")

    def update_status(self, message):
        """Update status bar"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        self.status_bar.config(text=f"[{timestamp}] {message}")


def main():
    """Main entry point"""
    root = tk.Tk()

    # Set icon (if available)
    try:
        root.iconbitmap("icon.ico")
    except:
        pass

    app = TreeDetectionApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
