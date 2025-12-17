# Quick Start Guide - Enhanced Fire Detection System

## ✨ What's New

Your custom configuration has been fully integrated with:
- Auto-downloading YOLO model
- Telegram notifications with photo alerts
- Enhanced real fire detection parameters
- More restrictive settings to reduce false positives

## 🚀 Installation & Setup

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

This will install:
- opencv-python (computer vision)
- numpy (numerical operations)
- torch & torchvision (AI/deep learning)
- ultralytics (YOLOv8)
- requests (Telegram integration)

### 2. Run the System

```bash
python main.py
```

**First Run:**
- YOLO model will auto-download (~6MB, one-time)
- Directories (recordings/, logs/) will be created
- Telegram will send "System Started" message to your chat

**Subsequent Runs:**
- System starts immediately (model already downloaded)

## 📱 Telegram Integration

**Your Configuration:**
- Bot Token: `8520172886:AAH80cExIgCMCEfTpEKrM61vs-Y0YFhuTGM`
- Chat ID: `7803447688`

**What Telegram Does:**
1. Sends startup notification when system begins
2. Sends "🚨 FIRE ALERT!" message when fire detected
3. Sends photo of detected fire with timestamp
4. Has 30-second cooldown between alerts (prevents spam)

## 🔥 Enhanced Fire Detection

Your configuration includes advanced parameters for detecting REAL fire:

### Color Detection
- **HSV Range:** (5-25 hue, 100-255 sat, 100-255 val)
- More restrictive than default (was 0-35)
- Focuses on orange-red fire colors

### Advanced Validation

1. **Intensity Check** (MIN_INTENSITY: 150)
   - Ensures detected regions are bright enough
   - Fire produces high intensity light

2. **Saturation Check** (MIN_SATURATION: 120)
   - Validates color vibrancy
   - Fire has highly saturated colors

3. **Shape Validation** (MAX_ASPECT_RATIO: 3.0)
   - Filters out elongated objects
   - Fire doesn't have extreme aspect ratios

4. **Edge Density** (MIN_EDGE_DENSITY: 0.1)
   - Detects flickering edges
   - Fire has dynamic, changing edges

5. **Multi-Frame Confirmation** (15 frames)
   - Requires detection in 15 consecutive frames
   - Much more reliable than default (3 frames)
   - Eliminates brief false positives

## ⚙️ Your Active Settings

```python
# Camera
CAMERA_INDEX = 0
CAMERA_WIDTH = 640
CAMERA_HEIGHT = 480
FPS = 30

# Fire Detection
FIRE_DETECTION_THRESHOLD = 0.01
MIN_FIRE_AREA = 500  # pixels
FIRE_CONFIRMATION_FRAMES = 15
FIRE_LOWER_HSV = (5, 100, 100)
FIRE_UPPER_HSV = (25, 255, 255)

# Advanced Parameters
MIN_INTENSITY = 150
MIN_SATURATION = 120
MAX_ASPECT_RATIO = 3.0
MIN_EDGE_DENSITY = 0.1

# AI
USE_AI_MODEL = True  # Auto-downloads yolov8n.pt
USE_HYBRID_MODE = True  # Uses both AI and CV

# Recording
RECORD_ON_DETECTION = True
RECORDING_DURATION = 10  # seconds

# Telegram
TELEGRAM_ENABLED = True
```

## 📹 Recording

When fire is detected:
- Video recording starts automatically
- Records for 10 seconds after detection
- Saves as MP4 in `recordings/` directory
- Filename: `fire_YYYYMMDD_HHMMSS.mp4`

## 🖼️ Screenshots

Fire alert screenshots are saved:
- Directory: `recordings/`
- Filename: `fire_alert_YYYYMMDD_HHMMSS.jpg`
- Automatically sent to Telegram

## 📊 Logs

System logs are saved to:
- Directory: `logs/`
- Filename: `fire_detection_YYYYMMDD_HHMMSS.log`
- Contains all events, detections, and errors

## ⌨️ Keyboard Controls

While running:
- `q` - Quit the application
- `s` - Save screenshot manually

## 🎯 Detection Pipeline

Your enhanced detection pipeline:

```
Frame Input
    ↓
Color Detection (HSV 5-25)
    ↓
Morphological Operations (noise reduction)
    ↓
Contour Detection
    ↓
✨ Intensity Check (≥150) ✨ NEW
    ↓
✨ Saturation Check (≥120) ✨ NEW
    ↓
✨ Aspect Ratio Check (≤3.0) ✨ NEW
    ↓
✨ Edge Density Check (≥0.1) ✨ NEW
    ↓
Motion/Flicker Analysis
    ↓
✨ 15-Frame Confirmation ✨ NEW
    ↓
Fire Detected!
    ↓
├─ Visual Alert (screen)
├─ Sound Alert (beep/WAV)
├─ Telegram Alert (text + photo)
└─ Video Recording (10s)
```

## 🔧 Troubleshooting

### YOLO Model Not Downloading
- Check internet connection
- First download needs ~6MB
- Will show: "Loading YOLOv8 model (will auto-download if needed)..."

### Telegram Not Working
- Verify bot token is correct
- Verify chat ID is correct
- Check internet connection
- System will log: "Telegram notifications enabled and ready"

### False Positives (detecting non-fire)
Your settings are already conservative, but you can adjust:
- Increase `FIRE_CONFIRMATION_FRAMES` (e.g., 20)
- Increase `MIN_INTENSITY` (e.g., 180)
- Increase `MIN_SATURATION` (e.g., 140)
- Narrow HSV range: `FIRE_LOWER_HSV = (8, 120, 120)`

### Missing Real Fire
If system doesn't detect actual fire:
- Decrease `FIRE_CONFIRMATION_FRAMES` (e.g., 10)
- Decrease `MIN_INTENSITY` (e.g., 130)
- Widen HSV range: `FIRE_UPPER_HSV = (30, 255, 255)`

## 📈 Performance

**Expected Performance:**
- FPS: ~15-30 (depends on hardware)
- CPU-only: Lower FPS, works fine
- GPU (CUDA): Higher FPS, recommended for AI

**System Requirements:**
- Python 3.7+
- Webcam/Camera
- 4GB+ RAM recommended
- GPU optional (but recommended for AI)

## 🔒 Security Note

Your Telegram bot token is in `config.py`. For production:
1. Use environment variables:
   ```python
   import os
   TELEGRAM_BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
   ```
2. Add `config.py` to `.gitignore` if sharing code
3. Never commit sensitive tokens to public repositories

## 📚 Files Overview

**Core Application:**
- `main.py` - Main application
- `fire_detector.py` - Detection logic (enhanced)
- `ai_model.py` - YOLO integration (auto-download)
- `alert.py` - Visual/audio alerts
- `telegram_notifier.py` - Telegram integration (NEW)
- `config.py` - Your custom configuration

**Documentation:**
- `README.md` - Full documentation
- `EXAMPLES.md` - Usage examples
- `ARCHITECTURE.md` - System design
- `QUICKSTART.md` - This file

## ✅ What's Working

After running `python main.py`:

1. ✅ YOLO model auto-downloads (first run)
2. ✅ Telegram "System Started" message sent
3. ✅ Camera opens and monitoring begins
4. ✅ Enhanced fire detection active (all 4 advanced parameters)
5. ✅ 15-frame confirmation reduces false positives
6. ✅ When fire detected:
   - Screen alert (red border, text)
   - Sound alert (beep)
   - Telegram text alert
   - Telegram photo alert
   - Video recording (10 seconds)
   - Log entry

## 🎉 You're Ready!

Everything is configured and ready. Just run:

```bash
python main.py
```

The system will handle everything automatically:
- Auto-download YOLO model
- Connect to Telegram
- Start monitoring
- Alert you when fire detected
- Send photos to Telegram

**Happy Fire Detecting! 🔥**
