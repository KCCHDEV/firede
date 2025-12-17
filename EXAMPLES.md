# Fire Detection System - Examples and Usage

This document provides examples and guidance for using the fire detection system.

## Quick Start

### 1. Basic Usage (with webcam)

```bash
# Install dependencies
pip install -r requirements.txt

# Run the system with default settings
python main.py
```

The system will:
- Open your default webcam (camera index 0)
- Start detecting fire using hybrid mode (AI + CV)
- Display real-time video with overlays
- Alert when fire is detected
- Record video automatically

### 2. Test System Without Camera

```bash
# Run system tests (no camera needed)
python test_system.py
```

This will verify:
- All modules can be imported
- Configuration is valid
- Dependencies are installed
- Directory structure is correct

## Configuration Examples

### Example 1: Using Different Camera

Edit `config.py`:

```python
CAMERA_INDEX = 1  # Use second camera
```

### Example 2: CV Only Mode (No AI)

For systems without GPU or when you don't need AI:

```python
USE_AI_MODEL = False  # Disable AI
USE_HYBRID_MODE = False  # Not needed without AI
```

### Example 3: AI Only Mode

For maximum accuracy with a trained model:

```python
USE_AI_MODEL = True
AI_MODEL_PATH = "path/to/your/trained_model.pt"
USE_HYBRID_MODE = False  # AI only, no CV
AI_CONFIDENCE_THRESHOLD = 0.6  # Adjust sensitivity
```

### Example 4: High Sensitivity (Detect Smaller Fires)

```python
MIN_FIRE_AREA = 200  # Lower threshold (default: 500)
FIRE_CONFIRMATION_FRAMES = 2  # Faster detection (default: 3)
FIRE_DETECTION_THRESHOLD = 0.6  # More sensitive
```

### Example 5: Low False Positives (More Conservative)

```python
MIN_FIRE_AREA = 1000  # Higher threshold
FIRE_CONFIRMATION_FRAMES = 5  # More frames to confirm
FIRE_DETECTION_THRESHOLD = 0.3  # Less sensitive
AI_CONFIDENCE_THRESHOLD = 0.7  # Higher AI confidence needed
```

### Example 6: Performance Mode (Low-End Hardware)

```python
CAMERA_WIDTH = 320
CAMERA_HEIGHT = 240
FPS = 15
USE_AI_MODEL = False  # Disable AI for performance
RECORD_ON_DETECTION = False  # Disable recording
```

### Example 7: Disable Recording

```python
RECORD_ON_DETECTION = False
```

### Example 8: Silent Mode (No Sound)

```python
ENABLE_SOUND_ALERT = False
```

### Example 9: Custom HSV Color Range

For different lighting conditions:

```python
# Wider range for varied lighting
FIRE_LOWER_HSV = (0, 100, 80)
FIRE_UPPER_HSV = (40, 255, 255)
```

## Training Custom AI Model

### Step 1: Prepare Dataset

1. Collect fire images/videos
2. Use [Roboflow](https://roboflow.com/) or [CVAT](https://www.cvat.ai/) to annotate
3. Export in YOLOv8 format

### Step 2: Train Model

```python
from ultralytics import YOLO

# Load base model
model = YOLO('yolov8n.pt')

# Train on your dataset
results = model.train(
    data='fire_dataset/data.yaml',  # Path to your dataset config
    epochs=100,
    imgsz=640,
    batch=16,
    name='fire_detector'
)

# Export best model
model = YOLO('runs/detect/fire_detector/weights/best.pt')
```

### Step 3: Use Trained Model

Edit `config.py`:

```python
USE_AI_MODEL = True
AI_MODEL_PATH = "runs/detect/fire_detector/weights/best.pt"
USE_HYBRID_MODE = True
AI_CONFIDENCE_THRESHOLD = 0.5
```

## Common Use Cases

### Use Case 1: Home Fire Detection

```python
# config.py settings
CAMERA_INDEX = 0
USE_HYBRID_MODE = True
MIN_FIRE_AREA = 500
FIRE_CONFIRMATION_FRAMES = 3
ENABLE_SOUND_ALERT = True
RECORD_ON_DETECTION = True
RECORDING_DURATION = 60  # Record 1 minute
```

### Use Case 2: Industrial Monitoring

```python
# config.py settings
CAMERA_INDEX = 0
USE_AI_MODEL = True
AI_MODEL_PATH = "models/industrial_fire.pt"  # Custom trained
USE_HYBRID_MODE = True
MIN_FIRE_AREA = 1000  # Larger fires
FIRE_CONFIRMATION_FRAMES = 5
ALERT_COOLDOWN = 10  # Less frequent alerts
RECORDING_DURATION = 120  # Record 2 minutes
```

### Use Case 3: Forest Fire Detection

```python
# config.py settings
CAMERA_INDEX = 0
USE_AI_MODEL = True
AI_MODEL_PATH = "models/forest_fire.pt"
MIN_FIRE_AREA = 2000  # Distant fires
FIRE_CONFIRMATION_FRAMES = 5
# Adjust HSV for outdoor lighting
FIRE_LOWER_HSV = (0, 100, 70)
FIRE_UPPER_HSV = (45, 255, 255)
```

### Use Case 4: Development/Testing

```python
# config.py settings
CAMERA_INDEX = 0
USE_AI_MODEL = True
USE_HYBRID_MODE = True
SHOW_FPS = True
SHOW_FRAME_COUNT = True
DISPLAY_CONFIDENCE = True
ENABLE_LOGGING = True
LOG_LEVEL = "DEBUG"
RECORD_ON_DETECTION = True
```

## Keyboard Controls

While the system is running:

- `q` - Quit the application
- `s` - Save current frame as screenshot

## Output Files

### Recorded Videos
- Location: `recordings/`
- Format: `fire_YYYYMMDD_HHMMSS.mp4`
- Example: `recordings/fire_20231215_143052.mp4`

### Screenshots
- Location: `recordings/`
- Format: `screenshot_YYYYMMDD_HHMMSS.jpg`
- Example: `recordings/screenshot_20231215_143052.jpg`

### Log Files
- Location: `logs/`
- Format: `fire_detection_YYYYMMDD_HHMMSS.log`
- Example: `logs/fire_detection_20231215_143052.log`

## Troubleshooting Scenarios

### Scenario 1: Too Many False Alarms from Orange Objects

**Problem**: System detects orange/red objects as fire

**Solution**:
```python
# Increase minimum area
MIN_FIRE_AREA = 800

# Require more frames to confirm
FIRE_CONFIRMATION_FRAMES = 5

# Use narrower color range
FIRE_LOWER_HSV = (0, 140, 120)
FIRE_UPPER_HSV = (30, 255, 255)
```

### Scenario 2: Missing Small Fires

**Problem**: System doesn't detect small flames

**Solution**:
```python
# Decrease minimum area
MIN_FIRE_AREA = 300

# Require fewer frames
FIRE_CONFIRMATION_FRAMES = 2

# Use wider color range
FIRE_LOWER_HSV = (0, 100, 80)
FIRE_UPPER_HSV = (40, 255, 255)
```

### Scenario 3: Poor Performance on Raspberry Pi

**Problem**: System is too slow

**Solution**:
```python
# Reduce resolution
CAMERA_WIDTH = 320
CAMERA_HEIGHT = 240

# Lower FPS
FPS = 10

# Disable AI
USE_AI_MODEL = False

# Disable recording
RECORD_ON_DETECTION = False
```

### Scenario 4: AI Not Detecting Fire

**Problem**: AI model doesn't detect fire

**Note**: Pre-trained YOLOv8 doesn't have fire classes. You need to:

1. Train a custom model (see "Training Custom AI Model" section)
2. Or disable AI and use CV only:

```python
USE_AI_MODEL = False
USE_HYBRID_MODE = False
```

## Advanced Integration

### Example: Add Email Alerts

Create `email_alert.py`:

```python
import smtplib
from email.mime.text import MIMEText

def send_email_alert():
    msg = MIMEText("Fire detected!")
    msg['Subject'] = 'ALERT: Fire Detected'
    msg['From'] = 'alerts@yourdomain.com'
    msg['To'] = 'admin@yourdomain.com'
    
    with smtplib.SMTP('smtp.gmail.com', 587) as server:
        server.starttls()
        server.login('your@email.com', 'password')
        server.send_message(msg)
```

Then modify `main.py` line where fire is detected:

```python
if fire_detected:
    self.alert_system.trigger_alert()
    # Add email alert
    send_email_alert()
```

### Example: Save Detection to Database

```python
import sqlite3
from datetime import datetime

def log_fire_detection(method, confidence):
    conn = sqlite3.connect('fire_detections.db')
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO detections (timestamp, method, confidence)
        VALUES (?, ?, ?)
    ''', (datetime.now().isoformat(), method, confidence))
    conn.commit()
    conn.close()
```

## Performance Tips

1. **Use GPU**: Install CUDA for PyTorch to enable GPU acceleration
2. **Reduce Resolution**: Lower resolution = faster processing
3. **Optimize Camera Settings**: Set camera to native resolution
4. **Close Other Apps**: Free up system resources
5. **Use SSD**: Faster disk I/O for recording

## Best Practices

1. **Test Your Environment**: Run test recordings in your actual environment
2. **Adjust for Lighting**: Different lighting needs different HSV values
3. **Train Custom Model**: For production use, train on your specific scenarios
4. **Use Hybrid Mode**: Best balance of accuracy and false positive reduction
5. **Monitor Logs**: Check logs regularly for system health
6. **Backup Recordings**: Ensure recordings are backed up regularly

## Safety Warning

⚠️ **IMPORTANT**: This system should be used as a **supplementary** fire detection method, NOT as a replacement for proper smoke detectors and fire alarm systems. Always follow local fire safety regulations and building codes.
