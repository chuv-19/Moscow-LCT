#!/usr/bin/env python3
"""
Build standalone executable for Tree Detection System
Creates a single .exe file (Windows) or binary (Mac/Linux) that includes everything
"""

import os
import sys
import platform
import subprocess
from pathlib import Path


def print_header(text):
    print("\n" + "=" * 60)
    print(text)
    print("=" * 60 + "\n")


def run_command(cmd, description):
    """Run a shell command and show progress"""
    print(f"⏳ {description}...")
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    if result.returncode == 0:
        print(f"✅ {description} - Success!")
        return True
    else:
        print(f"❌ {description} - Failed!")
        print(result.stderr)
        return False


def main():
    print_header("🚀 Tree Detection Executable Builder")

    script_dir = Path(__file__).parent.resolve()
    os.chdir(script_dir)

    # Detect OS
    os_name = platform.system()
    print(f"🖥️  Operating System: {os_name}")
    print(f"🐍 Python Version: {sys.version.split()[0]}")

    # Check if PyInstaller is installed
    print("\n📦 Checking PyInstaller...")
    try:
        import PyInstaller

        print(f"✅ PyInstaller found: {PyInstaller.__version__}")
    except ImportError:
        print("❌ PyInstaller not found. Installing...")
        if not run_command("pip install pyinstaller", "Installing PyInstaller"):
            print(
                "⚠️  Failed to install PyInstaller. Install manually: pip install pyinstaller"
            )
            return

    # Build configuration
    print_header("⚙️  Build Configuration")

    app_name = "TreeDetection"
    main_script = "app_mobile.py"

    print(f"📝 App Name: {app_name}")
    print(f"📄 Main Script: {main_script}")
    print(f"📁 Working Directory: {script_dir}")

    # Check if main script exists
    if not Path(main_script).exists():
        print(f"❌ Main script not found: {main_script}")
        return

    # Create build command
    print_header("🔨 Building Executable")

    # Base PyInstaller command
    build_cmd = [
        "pyinstaller",
        "--name",
        app_name,
        "--onefile",  # Single executable
        "--windowed" if os_name == "Windows" else "--console",  # GUI mode on Windows
        "--clean",  # Clean build
        "--noconfirm",  # Overwrite without asking
        # Add data files
        f"--add-data=config.ini{os.pathsep}.",
        f"--add-data=runs{os.pathsep}runs",
        f"--add-data=manifest.json{os.pathsep}.",
        # Hidden imports (packages not auto-detected)
        "--hidden-import=streamlit",
        "--hidden-import=ultralytics",
        "--hidden-import=torch",
        "--hidden-import=cv2",
        "--hidden-import=PIL",
        "--hidden-import=numpy",
        "--hidden-import=pandas",
        "--hidden-import=yaml",
        # Exclude unnecessary packages to reduce size
        "--exclude-module=matplotlib",
        "--exclude-module=IPython",
        "--exclude-module=notebook",
        # Entry point
        main_script,
    ]

    # Add icon if exists
    if Path("icon.ico").exists():
        build_cmd.insert(-1, "--icon=icon.ico")

    print(f"🔧 Command: {' '.join(build_cmd)}\n")

    # Run PyInstaller
    result = subprocess.run(build_cmd, capture_output=True, text=True)

    if result.returncode == 0:
        print("✅ Build successful!")

        # Find the executable
        if os_name == "Windows":
            exe_path = script_dir / "dist" / f"{app_name}.exe"
        else:
            exe_path = script_dir / "dist" / app_name

        if exe_path.exists():
            size_mb = exe_path.stat().st_size / 1024 / 1024
            print(f"\n✨ Executable created:")
            print(f"   📍 Location: {exe_path}")
            print(f"   📊 Size: {size_mb:.1f} MB")

            print_header("🎉 Build Complete!")
            print("To distribute:")
            print(f"1. Find your executable at: {exe_path}")
            print(f"2. Copy it to any computer (no Python needed!)")
            print(f"3. Double-click to run")
            print(f"4. App opens in browser automatically")

        else:
            print(f"⚠️  Executable not found at expected location: {exe_path}")
    else:
        print("❌ Build failed!")
        print("\nError output:")
        print(result.stderr)
        print("\nTry building manually with:")
        print(f"  {' '.join(build_cmd)}")


if __name__ == "__main__":
    main()
