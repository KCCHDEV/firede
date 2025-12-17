"""
Configuration file for Fire Detection System
"""
import os

# Camera settings
CAMERA_INDEX = 0  # 0 for default camera, change if you have multiple cameras
CAMERA_WIDTH = 640
CAMERA_HEIGHT = 480
FPS = 30

# Fire detection parameters
FIRE_DETECTION_THRESHOLD = 0.01  # Minimum fire area ratio (0.0 - 1.0)
MIN_FIRE_AREA = 500  # Minimum area in pixels to consider as fire
FIRE_CONFIRMATION_FRAMES = 15  # Number of consecutive frames needed to confirm fire

# Color ranges for fire detection (HSV) - More restrictive to reduce false positives
FIRE_LOWER_HSV = (5, 100, 100)  # Lower bound for fire color (more orange-red)
FIRE_UPPER_HSV = (25, 255, 255)  # Upper bound for fire color

# Advanced fire detection parameters
MIN_INTENSITY = 150  # Minimum average intensity in fire region
MIN_SATURATION = 120  # Minimum saturation for fire color
MAX_ASPECT_RATIO = 3.0  # Maximum aspect ratio (fire is usually not too elongated)
MIN_EDGE_DENSITY = 0.1  # Minimum edge density in fire region

# Alert settings
ENABLE_SOUND_ALERT = True
ENABLE_VISUAL_ALERT = True
ALERT_SOUND_PATH = "alert.wav"  # Path to alert sound file
ALERT_COOLDOWN = 5  # Seconds between alerts to avoid spam

# Recording settings
RECORD_ON_DETECTION = True
RECORDING_DURATION = 10  # seconds to record after fire detection
RECORDINGS_DIR = "recordings"
OUTPUT_DIR = "recordings"  # Alias for compatibility
RECORDINGS_FORMAT = "mp4"
OUTPUT_FORMAT = "mp4"  # Alias for compatibility

# Logging settings
LOG_DIR = "logs"
LOG_FILE = "fire_detection.log"
ENABLE_CONSOLE_LOG = True
ENABLE_LOGGING = True
LOG_LEVEL = "INFO"

# Display settings
SHOW_DETECTION_INFO = True
SHOW_FPS = True
SHOW_FRAME_COUNT = True
DISPLAY_CONFIDENCE = True
FONT_SCALE = 0.6
FONT_THICKNESS = 2

# AI Model settings
USE_AI_MODEL = True  # Enable AI-based detection
AI_MODEL_PATH = None  # Path to custom trained model (None = use pre-trained, auto-downloads)
AI_CONFIDENCE_THRESHOLD = 0.5  # Minimum confidence for AI detection (0.0 - 1.0)
USE_HYBRID_MODE = True  # Combine AI and traditional CV detection

# Telegram settings
TELEGRAM_ENABLED = True  # Enable Telegram notifications
TELEGRAM_BOT_TOKEN = "8520172886:AAH80cExIgCMCEfTpEKrM61vs-Y0YFhuTGM"  # Your Telegram bot token
TELEGRAM_CHAT_ID = "7803447688"  # Your Telegram chat ID

# Create necessary directories
os.makedirs(RECORDINGS_DIR, exist_ok=True)
os.makedirs(LOG_DIR, exist_ok=True)
