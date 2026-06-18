#!/usr/bin/env python3
"""
Configuration loader for YOLOv11 Tree Detection
Handles loading and validation of configuration from config.ini
"""

import configparser
from pathlib import Path
import os


class Config:
    """Configuration manager for inference application"""

    def __init__(self, config_file="config.ini"):
        self.config_file = Path(config_file)
        self.config = configparser.ConfigParser()

        # Default values
        self.defaults = {
            "model": {
                "model_path": "",
            },
            "paths": {
                "project_root": os.getcwd(),
                "runs_directory": "runs/detect",
                "test_images_directory": "dataset/test/images",
            },
            "inference": {
                "default_confidence": "0.25",
                "min_confidence": "0.05",
                "max_confidence": "0.95",
                "confidence_step": "0.05",
            },
            "display": {
                "max_example_images": "3",
                "default_image_width": "640",
            },
        }

        self.load_config()

    def load_config(self):
        """Load configuration from file or use defaults"""
        if self.config_file.exists():
            self.config.read(self.config_file)
        else:
            # Create config with defaults
            for section, options in self.defaults.items():
                if not self.config.has_section(section):
                    self.config.add_section(section)
                for key, value in options.items():
                    self.config.set(section, key, value)

    def get(self, section, option, fallback=None):
        """Get configuration value with fallback"""
        try:
            return self.config.get(section, option)
        except (configparser.NoSectionError, configparser.NoOptionError):
            if fallback is not None:
                return fallback
            return self.defaults.get(section, {}).get(option, "")

    def get_float(self, section, option, fallback=None):
        """Get float configuration value"""
        value = self.get(section, option, fallback)
        try:
            return float(value)
        except (ValueError, TypeError):
            if fallback is not None:
                return float(fallback)
            return 0.0

    def get_int(self, section, option, fallback=None):
        """Get integer configuration value"""
        value = self.get(section, option, fallback)
        try:
            return int(value)
        except (ValueError, TypeError):
            if fallback is not None:
                return int(fallback)
            return 0

    def get_path(self, section, option, fallback=None):
        """Get path configuration value and resolve it"""
        value = self.get(section, option, fallback)
        if not value:
            return None

        path = Path(value)

        # If relative path, make it relative to project root
        if not path.is_absolute():
            project_root = self.get_project_root()
            path = project_root / path

        return path

    def get_project_root(self):
        """Get project root directory"""
        root = self.get("paths", "project_root")
        if not root or root == os.getcwd():
            # Try to detect project root
            current = Path(__file__).parent.absolute()
            return current
        return Path(root)

    def get_model_path(self):
        """Get model path from config or find latest"""
        model_path = self.get("model", "model_path")

        if model_path and model_path.strip():
            path = self.get_path("model", "model_path")
            if path and path.exists():
                return str(path)

        # Try to find latest model
        return self.find_latest_model()

    def find_latest_model(self):
        """Find the most recently trained model"""
        runs_dir = self.get_path("paths", "runs_directory")

        if not runs_dir or not runs_dir.exists():
            return None

        train_dirs = [d for d in runs_dir.iterdir() if d.is_dir()]

        if not train_dirs:
            return None

        # Sort by modification time, get most recent
        latest_dir = max(train_dirs, key=lambda d: d.stat().st_mtime)
        best_model = latest_dir / "weights" / "best.pt"

        if best_model.exists():
            return str(best_model)

        # Try last.pt as fallback
        last_model = latest_dir / "weights" / "last.pt"
        if last_model.exists():
            return str(last_model)

        return None

    def get_test_images_dir(self):
        """Get test images directory"""
        return self.get_path("paths", "test_images_directory")

    def get_inference_settings(self):
        """Get all inference settings as a dictionary"""
        return {
            "default_confidence": self.get_float(
                "inference", "default_confidence", 0.25
            ),
            "min_confidence": self.get_float("inference", "min_confidence", 0.05),
            "max_confidence": self.get_float("inference", "max_confidence", 0.95),
            "confidence_step": self.get_float("inference", "confidence_step", 0.05),
        }

    def get_display_settings(self):
        """Get all display settings as a dictionary"""
        return {
            "max_example_images": self.get_int("display", "max_example_images", 3),
            "default_image_width": self.get_int("display", "default_image_width", 640),
        }

    def save_config(self):
        """Save current configuration to file"""
        with open(self.config_file, "w") as f:
            self.config.write(f)

    def create_default_config(self):
        """Create a default configuration file"""
        for section, options in self.defaults.items():
            if not self.config.has_section(section):
                self.config.add_section(section)
            for key, value in options.items():
                self.config.set(section, key, value)

        self.save_config()
        return self.config_file


def load_config(config_file="config.ini"):
    """Convenience function to load configuration"""
    return Config(config_file)


if __name__ == "__main__":
    # Test configuration loading
    config = load_config()

    print("Configuration Test")
    print("=" * 50)
    print(f"Config file: {config.config_file}")
    print(f"Project root: {config.get_project_root()}")
    print(f"Model path: {config.get_model_path()}")
    print(f"Test images: {config.get_test_images_dir()}")
    print(f"Inference settings: {config.get_inference_settings()}")
    print(f"Display settings: {config.get_display_settings()}")
