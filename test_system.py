"""
Test script for Fire Detection System (without camera)
Tests basic functionality of modules
"""
import sys
import os

print("=" * 60)
print("Fire Detection System - Module Tests")
print("=" * 60)
print()

# Test 1: Configuration
print("Test 1: Configuration Module")
print("-" * 40)
try:
    import config
    print("✓ config.py imported successfully")
    print(f"  Camera: {config.CAMERA_INDEX}")
    print(f"  Resolution: {config.CAMERA_WIDTH}x{config.CAMERA_HEIGHT}")
    print(f"  AI Enabled: {config.USE_AI_MODEL}")
    print(f"  Hybrid Mode: {config.USE_HYBRID_MODE}")
except Exception as e:
    print(f"✗ Error: {e}")
    sys.exit(1)

print()

# Test 2: Check directory structure
print("Test 2: Directory Structure")
print("-" * 40)
try:
    recordings_exist = os.path.exists(config.OUTPUT_DIR)
    logs_exist = os.path.exists(config.LOG_DIR)
    print(f"✓ Recordings directory: {'exists' if recordings_exist else 'will be created'}")
    print(f"✓ Logs directory: {'exists' if logs_exist else 'will be created'}")
except Exception as e:
    print(f"✗ Error: {e}")
    sys.exit(1)

print()

# Test 3: Check if dependencies are available
print("Test 3: Dependencies Check")
print("-" * 40)
deps = {
    'opencv-python': 'cv2',
    'numpy': 'numpy',
    'torch': 'torch',
    'ultralytics': 'ultralytics',
    'pygame (optional)': 'pygame'
}

missing = []
for name, module in deps.items():
    try:
        __import__(module)
        print(f"✓ {name}")
    except ImportError:
        print(f"✗ {name} - Not installed")
        missing.append(name)

if missing:
    print()
    print("⚠ Missing dependencies. Install with:")
    print("  pip install -r requirements.txt")
    if 'pygame (optional)' in missing:
        print("  pip install pygame  # For sound alerts")

print()

# Test 4: Module imports (if dependencies available)
print("Test 4: Module Imports")
print("-" * 40)

try:
    from ai_model import AIFireDetector
    print("✓ ai_model.py")
except Exception as e:
    print(f"✗ ai_model.py: {e}")

try:
    from fire_detector import FireDetector
    print("✓ fire_detector.py")
except Exception as e:
    print(f"✗ fire_detector.py: {e}")

try:
    from alert import AlertSystem
    print("✓ alert.py")
except Exception as e:
    print(f"✗ alert.py: {e}")

print()

# Test 5: Syntax check all Python files
print("Test 5: Python Syntax Validation")
print("-" * 40)
python_files = ['main.py', 'config.py', 'ai_model.py', 'fire_detector.py', 'alert.py']
all_valid = True

for pyfile in python_files:
    try:
        with open(pyfile, 'r') as f:
            compile(f.read(), pyfile, 'exec')
        print(f"✓ {pyfile}")
    except SyntaxError as e:
        print(f"✗ {pyfile}: Line {e.lineno}: {e.msg}")
        all_valid = False
    except Exception as e:
        print(f"✗ {pyfile}: {e}")
        all_valid = False

print()
print("=" * 60)
if all_valid and not missing:
    print("✓ All tests passed! System is ready to use.")
    print()
    print("To run the system:")
    print("  python main.py")
elif all_valid:
    print("⚠ Syntax valid but missing dependencies.")
    print()
    print("Install dependencies:")
    print("  pip install -r requirements.txt")
else:
    print("✗ Some tests failed. Please fix the issues above.")

print("=" * 60)
