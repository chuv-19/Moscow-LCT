"""
YOLOv11 Inference GUI for Tree Detection
Simple GUI application for selecting images and running inference
"""

import tkinter as tk
from tkinter import filedialog, messagebox
from tkinter import ttk
from PIL import Image, ImageTk
import cv2
import numpy as np
from pathlib import Path
from ultralytics import YOLO
import torch
import os

# Fix for PyTorch 2.6+ weights_only security change

try:
    from ultralytics.nn.tasks import DetectionModel

    torch.serialization.add_safe_globals([DetectionModel])
except Exception:
    pass  # Older PyTorch versions don't have this


class YOLOInferenceGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("YOLOv11 Tree Detection - Inference")
        self.root.geometry("1200x800")

        # Model path
        self.model = None
        self.current_image = None
        self.current_image_path = None
        self.result_image = None

        # Create GUI components
        self.create_widgets()

        # Try to load the latest trained model
        self.auto_load_model()

    def create_widgets(self):
        # Main container
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        # Configure grid weights
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        main_frame.rowconfigure(2, weight=1)

        # Title
        title_label = ttk.Label(
            main_frame, text="YOLOv11 Tree Detection", font=("Arial", 16, "bold")
        )
        title_label.grid(row=0, column=0, columnspan=3, pady=10)

        # Control Panel
        control_frame = ttk.LabelFrame(main_frame, text="Controls", padding="10")
        control_frame.grid(row=1, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=5)

        # Model selection
        ttk.Label(control_frame, text="Model:").grid(
            row=0, column=0, padx=5, sticky=tk.W
        )
        self.model_path_var = tk.StringVar(value="No model loaded")
        model_label = ttk.Label(
            control_frame, textvariable=self.model_path_var, foreground="blue"
        )
        model_label.grid(row=0, column=1, padx=5, sticky=tk.W)
        ttk.Button(control_frame, text="Load Model", command=self.load_model).grid(
            row=0, column=2, padx=5
        )

        # Image selection
        ttk.Button(
            control_frame, text="Select Image", command=self.select_image, width=15
        ).grid(row=1, column=0, padx=5, pady=5)

        # Inference button
        self.inference_btn = ttk.Button(
            control_frame,
            text="Run Detection",
            command=self.run_inference,
            width=15,
            state="disabled",
        )
        self.inference_btn.grid(row=1, column=1, padx=5, pady=5)

        # Confidence threshold
        ttk.Label(control_frame, text="Confidence:").grid(row=1, column=2, padx=5)
        self.confidence_var = tk.DoubleVar(value=0.25)
        confidence_spin = ttk.Spinbox(
            control_frame,
            from_=0.0,
            to=1.0,
            increment=0.05,
            textvariable=self.confidence_var,
            width=10,
        )
        confidence_spin.grid(row=1, column=3, padx=5)

        # Save result button
        self.save_btn = ttk.Button(
            control_frame,
            text="Save Result",
            command=self.save_result,
            width=15,
            state="disabled",
        )
        self.save_btn.grid(row=1, column=4, padx=5, pady=5)

        # Image display area
        display_frame = ttk.Frame(main_frame)
        display_frame.grid(
            row=2, column=0, columnspan=3, sticky=(tk.W, tk.E, tk.N, tk.S), pady=5
        )
        display_frame.columnconfigure(0, weight=1)
        display_frame.columnconfigure(1, weight=1)
        display_frame.rowconfigure(0, weight=1)

        # Original image
        original_frame = ttk.LabelFrame(
            display_frame, text="Original Image", padding="5"
        )
        original_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), padx=5)
        original_frame.columnconfigure(0, weight=1)
        original_frame.rowconfigure(0, weight=1)

        self.original_canvas = tk.Canvas(
            original_frame, bg="gray", width=500, height=500
        )
        self.original_canvas.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        # Result image
        result_frame = ttk.LabelFrame(
            display_frame, text="Detection Result", padding="5"
        )
        result_frame.grid(row=0, column=1, sticky=(tk.W, tk.E, tk.N, tk.S), padx=5)
        result_frame.columnconfigure(0, weight=1)
        result_frame.rowconfigure(0, weight=1)

        self.result_canvas = tk.Canvas(result_frame, bg="gray", width=500, height=500)
        self.result_canvas.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        # Status bar
        status_frame = ttk.Frame(main_frame)
        status_frame.grid(row=3, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=5)

        self.status_var = tk.StringVar(
            value="Ready. Please load a model and select an image."
        )
        status_label = ttk.Label(
            status_frame, textvariable=self.status_var, relief=tk.SUNKEN, anchor=tk.W
        )
        status_label.pack(fill=tk.X)

        # Results info
        info_frame = ttk.LabelFrame(main_frame, text="Detection Info", padding="10")
        info_frame.grid(row=4, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=5)

        self.info_text = tk.Text(info_frame, height=4, width=80, state="disabled")
        self.info_text.pack(fill=tk.BOTH, expand=True)

    def auto_load_model(self):
        """Automatically load the most recent trained model"""
        # Use relative path from script location
        script_dir = Path(__file__).parent.resolve()
        runs_dir = script_dir / "runs" / "detect"

        if runs_dir.exists():
            # Find all training directories
            train_dirs = [d for d in runs_dir.iterdir() if d.is_dir()]

            if train_dirs:
                # Sort by modification time, get most recent
                latest_dir = max(train_dirs, key=lambda d: d.stat().st_mtime)
                best_model = latest_dir / "weights" / "best.pt"

                if best_model.exists():
                    try:
                        self.model = YOLO(str(best_model))
                        self.model_path_var.set(
                            f".../{latest_dir.name}/weights/best.pt"
                        )
                        self.status_var.set(f"Model loaded: {latest_dir.name}")
                        return
                    except Exception as e:
                        print(f"Could not auto-load model: {e}")

        self.status_var.set(
            "No trained model found. Please train a model first or load one manually."
        )

    def load_model(self):
        """Load a YOLO model"""
        # Use relative path from script location
        script_dir = Path(__file__).parent.resolve()
        initial_dir = script_dir / "runs" / "detect"

        model_path = filedialog.askopenfilename(
            title="Select YOLO Model",
            filetypes=[("PyTorch Model", "*.pt"), ("All Files", "*.*")],
            initialdir=str(initial_dir) if initial_dir.exists() else str(script_dir),
        )

        if model_path:
            try:
                self.model = YOLO(model_path)
                self.model_path_var.set(
                    f".../{Path(model_path).parent.parent.name}/weights/{Path(model_path).name}"
                )
                self.status_var.set(
                    f"Model loaded successfully: {Path(model_path).name}"
                )

                if self.current_image_path:
                    self.inference_btn.config(state="normal")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to load model:\n{str(e)}")
                self.status_var.set("Error loading model")

    def select_image(self):
        """Select an image for inference"""
        image_path = filedialog.askopenfilename(
            title="Select Image",
            filetypes=[
                ("Image Files", "*.jpg *.jpeg *.png *.bmp *.gif *.tiff"),
                ("All Files", "*.*"),
            ],
        )

        if image_path:
            try:
                self.current_image_path = image_path
                self.current_image = cv2.imread(image_path)

                if self.current_image is None:
                    raise ValueError("Could not read image")

                # Display original image
                self.display_image(self.current_image, self.original_canvas)

                # Clear result canvas
                self.result_canvas.delete("all")
                self.result_image = None

                # Update status
                self.status_var.set(f"Image loaded: {Path(image_path).name}")

                # Enable inference button if model is loaded
                if self.model is not None:
                    self.inference_btn.config(state="normal")

                # Clear info
                self.update_info("")

            except Exception as e:
                messagebox.showerror("Error", f"Failed to load image:\n{str(e)}")
                self.status_var.set("Error loading image")

    def run_inference(self):
        """Run YOLO inference on the selected image"""
        if self.model is None:
            messagebox.showwarning("Warning", "Please load a model first")
            return

        if self.current_image_path is None:
            messagebox.showwarning("Warning", "Please select an image first")
            return

        try:
            self.status_var.set("Running inference...")
            self.root.update()

            # Run inference
            conf_threshold = self.confidence_var.get()
            results = self.model(
                self.current_image_path, conf=conf_threshold, verbose=False
            )

            # Get the result image with bounding boxes
            result_img = results[0].plot()
            self.result_image = result_img

            # Display result
            self.display_image(result_img, self.result_canvas)

            # Get detection info
            boxes = results[0].boxes
            num_detections = len(boxes)

            info_text = f"Detections: {num_detections} trees found\n"
            info_text += f"Confidence threshold: {conf_threshold}\n"

            if num_detections > 0:
                confidences = boxes.conf.cpu().numpy()
                info_text += f"Confidence range: {confidences.min():.3f} - {confidences.max():.3f}\n"
                info_text += f"Average confidence: {confidences.mean():.3f}"
            else:
                info_text += "No trees detected above confidence threshold"

            self.update_info(info_text)
            self.status_var.set(f"Inference complete: {num_detections} trees detected")

            # Enable save button
            self.save_btn.config(state="normal")

        except Exception as e:
            messagebox.showerror("Error", f"Inference failed:\n{str(e)}")
            self.status_var.set("Inference failed")

    def display_image(self, img, canvas):
        """Display an image on a canvas"""
        # Convert BGR to RGB
        img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

        # Get canvas size
        canvas_width = canvas.winfo_width()
        canvas_height = canvas.winfo_height()

        # Use default size if canvas not yet rendered
        if canvas_width <= 1:
            canvas_width = 500
            canvas_height = 500

        # Resize image to fit canvas while maintaining aspect ratio
        img_height, img_width = img_rgb.shape[:2]
        scale = min(canvas_width / img_width, canvas_height / img_height)
        new_width = int(img_width * scale)
        new_height = int(img_height * scale)

        img_resized = cv2.resize(img_rgb, (new_width, new_height))

        # Convert to PhotoImage
        img_pil = Image.fromarray(img_resized)
        photo = ImageTk.PhotoImage(img_pil)

        # Display on canvas
        canvas.delete("all")
        canvas.create_image(
            canvas_width // 2, canvas_height // 2, image=photo, anchor=tk.CENTER
        )

        # Keep a reference to prevent garbage collection
        canvas.image = photo

    def update_info(self, text):
        """Update the info text widget"""
        self.info_text.config(state="normal")
        self.info_text.delete(1.0, tk.END)
        self.info_text.insert(1.0, text)
        self.info_text.config(state="disabled")

    def save_result(self):
        """Save the result image"""
        if self.result_image is None:
            messagebox.showwarning("Warning", "No result to save")
            return

        save_path = filedialog.asksaveasfilename(
            title="Save Result",
            defaultextension=".jpg",
            filetypes=[("JPEG", "*.jpg"), ("PNG", "*.png"), ("All Files", "*.*")],
        )

        if save_path:
            try:
                cv2.imwrite(save_path, self.result_image)
                self.status_var.set(f"Result saved: {Path(save_path).name}")
                messagebox.showinfo("Success", "Result saved successfully!")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to save result:\n{str(e)}")


def main():
    root = tk.Tk()
    app = YOLOInferenceGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()
