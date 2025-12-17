"""
Configuration file for Fire Detection System
"""

# Camera Settings
CAMERA_INDEX = 0  # 0 for default camera, 1, 2, ... for other cameras
CAMERA_WIDTH = 640
CAMERA_HEIGHT = 480
FPS = 30

# AI Model Settings
# ⚠️ IMPORTANT: Pre-trained YOLOv8 does NOT have fire classes!
# For AI detection to work, you MUST train a custom model and set AI_MODEL_PATH
# OR set USE_AI_MODEL = False to use CV-only mode (recommended for first-time users)
USE_AI_MODEL = False  # Enable/Disable AI detection (set False until you have a custom trained model)
AI_MODEL_PATH = None  # Path to custom trained YOLOv8 model (train your own for fire detection)
AI_CONFIDENCE_THRESHOLD = 0.5  # Minimum confidence for AI detection (0.0 - 1.0)
USE_HYBRID_MODE = False  # Use both AI and CV (True) or CV only (False). Set True when you have custom model

# Traditional Computer Vision Settings
FIRE_DETECTION_THRESHOLD = 0.5  # Sensitivity for fire detection (0.0 - 1.0)
MIN_FIRE_AREA = 500  # Minimum area in pixels to consider as fire
FIRE_CONFIRMATION_FRAMES = 3  # Number of consecutive frames needed to confirm fire

# HSV Color Range for Fire Detection
# Lower bound for fire color (Hue, Saturation, Value)
FIRE_LOWER_HSV = (0, 120, 100)
# Upper bound for fire color
FIRE_UPPER_HSV = (35, 255, 255)

# Alert Settings
ENABLE_SOUND_ALERT = True  # Enable/Disable sound alerts
ALERT_SOUND_PATH = "alert.wav"  # Path to alert sound file
ALERT_COOLDOWN = 5  # Seconds between alerts to avoid spam

# Recording Settings
RECORD_ON_DETECTION = True  # Record video when fire is detected
RECORDING_DURATION = 30  # Duration in seconds to record after detection
OUTPUT_DIR = "recordings"  # Directory to save recorded videos
OUTPUT_FORMAT = "mp4"  # Video format

# Logging Settings
ENABLE_LOGGING = True  # Enable/Disable logging
LOG_DIR = "logs"  # Directory to save log files
LOG_LEVEL = "INFO"  # Logging level: DEBUG, INFO, WARNING, ERROR

# Display Settings
SHOW_FPS = True  # Show FPS counter on display
SHOW_FRAME_COUNT = True  # Show frame count on display
DISPLAY_CONFIDENCE = True  # Show confidence scores on detections
