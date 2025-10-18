#!/usr/bin/env python3
"""
Simple test script to check if all required dependencies are available
"""

def test_dependencies():
    missing_deps = []
    
    try:
        import flask
        print("✓ Flask imported successfully")
    except ImportError:
        missing_deps.append("flask")
        print("✗ Flask not found")
    
    try:
        import flask_cors
        print("✓ Flask-CORS imported successfully")
    except ImportError:
        missing_deps.append("flask-cors")
        print("✗ Flask-CORS not found")
    
    try:
        import librosa
        print("✓ librosa imported successfully")
    except ImportError:
        missing_deps.append("librosa")
        print("✗ librosa not found")
    
    try:
        import noisereduce
        print("✓ noisereduce imported successfully")
    except ImportError:
        missing_deps.append("noisereduce")
        print("✗ noisereduce not found")
    
    try:
        import soundfile
        print("✓ soundfile imported successfully")
    except ImportError:
        missing_deps.append("soundfile")
        print("✗ soundfile not found")
    
    try:
        import numpy
        print("✓ numpy imported successfully")
    except ImportError:
        missing_deps.append("numpy")
        print("✗ numpy not found")
    
    try:
        import scipy
        print("✓ scipy imported successfully")
    except ImportError:
        missing_deps.append("scipy")
        print("✗ scipy not found")
    
    if missing_deps:
        print(f"\n❌ Missing dependencies: {', '.join(missing_deps)}")
        print("\nTo install missing dependencies, run:")
        print("pip install " + " ".join(missing_deps))
        return False
    else:
        print("\n✅ All dependencies are available!")
        return True

if __name__ == "__main__":
    test_dependencies()
