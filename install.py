#!/usr/bin/env python3
"""
Installation script for BG Noise Remover
"""

import subprocess
import sys
import os

def run_command(command):
    """Run a command and return success status"""
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print(f"✓ Success: {command}")
        return True
    except subprocess.CalledProcessError as e:
        print(f"✗ Error: {command}")
        print(f"  Error message: {e.stderr}")
        return False

def install_dependencies():
    """Install required dependencies"""
    print("Installing BG Noise Remover dependencies...")
    
    # Try installing with pip
    packages = [
        "flask",
        "flask-cors", 
        "librosa",
        "noisereduce",
        "soundfile",
        "numpy",
        "scipy"
    ]
    
    success_count = 0
    for package in packages:
        if run_command(f"pip install {package}"):
            success_count += 1
    
    print(f"\nInstalled {success_count}/{len(packages)} packages successfully")
    
    if success_count == len(packages):
        print("✅ All dependencies installed successfully!")
        return True
    else:
        print("⚠️  Some dependencies failed to install. You may need to install them manually.")
        print("\nTry running:")
        print("pip install --upgrade pip")
        print("pip install -r requirements.txt")
        return False

def create_directories():
    """Create necessary directories"""
    directories = ['uploads', 'outputs', 'templates']
    
    for directory in directories:
        if not os.path.exists(directory):
            os.makedirs(directory)
            print(f"✓ Created directory: {directory}")
        else:
            print(f"✓ Directory exists: {directory}")

def main():
    print("🎵 BG Noise Remover Installation Script")
    print("=" * 40)
    
    # Create directories
    print("\n1. Creating directories...")
    create_directories()
    
    # Install dependencies
    print("\n2. Installing dependencies...")
    if install_dependencies():
        print("\n🎉 Installation completed successfully!")
        print("\nTo run the application:")
        print("python app.py")
        print("\nThen open your browser to: http://localhost:5000")
    else:
        print("\n❌ Installation completed with errors.")
        print("Please check the error messages above and install missing dependencies manually.")

if __name__ == "__main__":
    main()
