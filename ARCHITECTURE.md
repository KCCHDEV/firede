# Fire Detection System Architecture

## System Overview

```
┌─────────────────────────────────────────────────────────────────┐
│                     Fire Detection System                        │
└─────────────────────────────────────────────────────────────────┘

┌──────────────┐
│   Camera     │
│   Input      │
└──────┬───────┘
       │
       ▼
┌──────────────────────────────────────────────────────────────────┐
│                      Main Application (main.py)                   │
│  ┌────────────────────────────────────────────────────────────┐  │
│  │  • Camera Management                                        │  │
│  │  • Frame Processing Loop                                    │  │
│  │  • Video Recording Control                                  │  │
│  │  • Display & UI Management                                  │  │
│  │  • FPS & Performance Monitoring                             │  │
│  └────────────────────────────────────────────────────────────┘  │
└───────────┬──────────────────────────────────────────────────────┘
            │
            ▼
┌──────────────────────────────────────────────────────────────────┐
│               Fire Detector (fire_detector.py)                    │
│  ┌────────────────────────────────────────────────────────────┐  │
│  │  • Detection Orchestration                                  │  │
│  │  • Hybrid Mode Logic                                        │  │
│  │  • Frame Confirmation System                                │  │
│  │  • Result Aggregation                                       │  │
│  └────────────────────────────────────────────────────────────┘  │
└───────┬───────────────────────────────────────────┬──────────────┘
        │                                           │
        ▼                                           ▼
┌──────────────────────────┐          ┌──────────────────────────┐
│  CV Detection            │          │  AI Detection            │
│  (fire_detector.py)      │          │  (ai_model.py)           │
│ ┌──────────────────────┐ │          │ ┌──────────────────────┐ │
│ │ • Color Detection    │ │          │ │ • YOLOv8 Model       │ │
│ │   (HSV)              │ │          │ │ • GPU Acceleration   │ │
│ │ • Morphology Ops     │ │          │ │ • Fire Class         │ │
│ │ • Contour Analysis   │ │          │ │   Detection          │ │
│ │ • Intensity Check    │ │          │ │ • Confidence         │ │
│ │ • Motion Analysis    │ │          │ │   Scoring            │ │
│ └──────────────────────┘ │          │ └──────────────────────┘ │
└──────────────────────────┘          └──────────────────────────┘
        │                                           │
        └───────────────────┬───────────────────────┘
                            │
                            ▼
            ┌───────────────────────────────┐
            │   Fire Detected?              │
            └───────────┬───────────────────┘
                        │
                        ├─────────────────────────────────┐
                        │                                 │
                        ▼                                 ▼
        ┌───────────────────────────┐     ┌───────────────────────────┐
        │   Alert System            │     │   Recording System        │
        │   (alert.py)              │     │   (main.py)               │
        │  ┌─────────────────────┐  │     │  ┌─────────────────────┐  │
        │  │ • Visual Alerts     │  │     │  │ • Video Recording   │  │
        │  │ • Sound Alerts      │  │     │  │ • MP4 Output        │  │
        │  │ • Screen Overlays   │  │     │  │ • Auto Start/Stop   │  │
        │  │ • Alert Cooldown    │  │     │  │ • Duration Control  │  │
        │  └─────────────────────┘  │     │  └─────────────────────┘  │
        └───────────────────────────┘     └───────────────────────────┘
                        │                                 │
                        └─────────────┬───────────────────┘
                                      │
                                      ▼
                        ┌─────────────────────────┐
                        │   Logging System        │
                        │  • Event Logs           │
                        │  • Error Tracking       │
                        │  • Performance Metrics  │
                        └─────────────────────────┘
```

## Component Details

### 1. Configuration (config.py)
- Centralized configuration management
- Camera settings
- AI model parameters
- CV detection thresholds
- Alert and recording settings
- Display options

### 2. Main Application (main.py)
**Responsibilities:**
- Initialize all components
- Open and manage camera
- Main processing loop
- Coordinate between components
- Handle user input
- Display management

**Key Methods:**
- `open_camera()` - Initialize camera device
- `start_recording()` / `stop_recording()` - Video recording control
- `run()` - Main event loop
- `draw_info()` - Overlay information on display
- `cleanup()` - Resource cleanup

### 3. Fire Detector (fire_detector.py)
**Responsibilities:**
- Orchestrate fire detection
- Combine AI and CV results
- Implement confirmation system
- Manage detection state

**Detection Pipeline:**
```
Frame → CV Detection ──┐
                       ├──→ Hybrid Logic → Confirmation → Result
Frame → AI Detection ──┘
```

**Key Methods:**
- `detect_fire_cv()` - Traditional CV detection
- `detect_fire_ai()` - AI-based detection
- `detect()` - Main detection coordinator

### 4. AI Model (ai_model.py)
**Responsibilities:**
- YOLOv8 model management
- GPU acceleration
- Fire class detection
- Confidence scoring

**Features:**
- Custom model support
- Pre-trained model fallback
- CUDA/CPU auto-selection
- Configurable confidence threshold

**Detection Process:**
```
Frame → YOLOv8 → Object Detection → Filter Fire Classes → Bounding Boxes
```

### 5. Alert System (alert.py)
**Responsibilities:**
- Visual alert rendering
- Sound alert playback
- Alert state management
- Cooldown control

**Features:**
- Red border overlay
- Pulsing alert text
- WAV file playback
- Generated beep fallback
- Non-blocking audio

### 6. Computer Vision Detection
**Multi-Stage Pipeline:**

```
1. Color Detection (HSV)
   Frame → HSV Conversion → Color Mask
   └─ Range: (0,120,100) to (35,255,255)

2. Brightness Analysis
   Frame → Grayscale → Threshold → Bright Mask
   └─ Threshold: 200

3. Morphological Operations
   Mask → Opening → Closing → Clean Mask
   └─ Kernel: 5x5 Ellipse, 2 iterations

4. Contour Detection
   Clean Mask → Find Contours → Filter by Area
   └─ Min Area: 500 pixels
   └─ Aspect Ratio: 0.2 - 5.0

5. Motion Analysis
   Current Frame - Previous Frame → Motion Score
   └─ Min Motion: 5 (for flicker detection)

6. Confirmation
   Detection History → Require N Frames → Confirmed
   └─ Default: 3 consecutive frames
```

## Data Flow

### Input Flow
```
Camera → Frame Capture → BGR Image → Detection Pipeline
```

### Detection Flow
```
BGR Frame
    ├→ CV Pipeline
    │   ├→ HSV Conversion
    │   ├→ Color Masking
    │   ├→ Morphology
    │   ├→ Contour Analysis
    │   └→ Motion Check
    │
    └→ AI Pipeline
        ├→ YOLOv8 Inference
        ├→ Object Detection
        └→ Fire Classification
```

### Output Flow
```
Detection Results
    ├→ Display (with overlays)
    ├→ Alert System (if fire detected)
    ├→ Recording System (if fire detected)
    └→ Logging System (events)
```

## Configuration Flow

```
config.py
    ├→ Camera Settings → main.py
    ├→ AI Settings → ai_model.py
    ├→ CV Settings → fire_detector.py
    ├→ Alert Settings → alert.py
    └→ Recording Settings → main.py
```

## Threading Model

```
Main Thread
    └─ GUI & Main Loop
        ├─ Camera Capture
        ├─ Detection Processing
        ├─ Display Update
        └─ User Input

Background Threads
    ├─ Sound Alert Playback (daemon)
    └─ Video Recording (optional)
```

## File System Structure

```
firede/
├── Source Files
│   ├── main.py              - Entry point
│   ├── fire_detector.py     - Detection logic
│   ├── ai_model.py          - AI detection
│   ├── alert.py             - Alert system
│   └── config.py            - Configuration
│
├── Documentation
│   ├── README.md            - Main documentation
│   ├── EXAMPLES.md          - Usage examples
│   └── ARCHITECTURE.md      - This file
│
├── Testing
│   └── test_system.py       - System validation
│
├── Output Directories
│   ├── recordings/          - Video recordings
│   │   └── fire_*.mp4
│   └── logs/                - Log files
│       └── fire_detection_*.log
│
└── Configuration
    ├── requirements.txt     - Dependencies
    └── .gitignore          - Git exclusions
```

## Performance Considerations

### Optimization Strategies
1. **Resolution Scaling**: Lower resolution = faster processing
2. **GPU Acceleration**: CUDA for AI inference
3. **Frame Skipping**: Process every Nth frame (optional)
4. **Efficient Algorithms**: Optimized OpenCV operations
5. **Caching**: Reuse previous frame data for motion analysis

### Bottlenecks
- Camera frame rate
- AI inference time (GPU/CPU dependent)
- Video encoding (recording)
- Display rendering

### Memory Usage
- Frame buffers
- YOLOv8 model weights (~6-100MB depending on model)
- Video recording buffer
- Detection history (minimal)

## Security Considerations

1. **Input Validation**: All config values validated
2. **Resource Limits**: Frame buffer size controlled
3. **Safe File Operations**: Proper error handling
4. **No External Network**: Runs locally only
5. **Clean Shutdown**: Proper resource cleanup

## Extensibility Points

### Adding New Detection Methods
1. Create new method in `fire_detector.py`
2. Add to detection pipeline
3. Update hybrid logic

### Adding New Alert Types
1. Extend `AlertSystem` class
2. Add new alert trigger in main loop
3. Configure in `config.py`

### Custom AI Models
1. Train YOLOv8 model
2. Set `AI_MODEL_PATH` in config
3. Adjust confidence threshold

### Integration Points
- Email/SMS alerts (add in alert.py)
- Database logging (add in main.py)
- Cloud storage (add in recording logic)
- REST API (create new module)

## Dependencies Graph

```
main.py
    ├─→ config.py
    ├─→ fire_detector.py
    │   ├─→ config.py
    │   ├─→ ai_model.py
    │   │   ├─→ ultralytics (YOLO)
    │   │   ├─→ torch
    │   │   └─→ numpy
    │   ├─→ cv2 (OpenCV)
    │   └─→ numpy
    ├─→ alert.py
    │   ├─→ config.py
    │   ├─→ pygame (optional)
    │   ├─→ cv2
    │   └─→ numpy
    └─→ cv2 (OpenCV)
```

## Error Handling Strategy

1. **Graceful Degradation**
   - AI not available → Fall back to CV
   - pygame not available → Disable sound
   - Camera fails → Clean error message

2. **Logging**
   - All errors logged to file
   - Console output for critical issues

3. **Recovery**
   - Automatic retry for transient errors
   - Clean shutdown on fatal errors
   - Resource cleanup guaranteed

## Testing Strategy

1. **Unit Testing**: Individual components (future)
2. **Integration Testing**: Component interaction
3. **System Testing**: End-to-end validation (`test_system.py`)
4. **Performance Testing**: FPS monitoring built-in
5. **Manual Testing**: Real-world fire scenarios

---

This architecture provides a modular, maintainable, and extensible fire detection system suitable for various deployment scenarios.
