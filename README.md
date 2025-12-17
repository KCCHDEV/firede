# 🔥 Fire Detection System

ระบบตรวจจับไฟแบบ Real-time โดยใช้กล้องคอมพิวเตอร์, Computer Vision และ **AI/Deep Learning**

## ✨ Features

- 🤖 **AI-based Detection**: ใช้ YOLOv8 และ Deep Learning สำหรับตรวจจับไฟ
- 🔍 ตรวจจับไฟแบบ Real-time จากกล้องคอมพิวเตอร์
- 🎨 ใช้ Color-based detection และ Motion analysis
- 🔄 **Hybrid Mode**: รวม AI และ Traditional CV เพื่อความแม่นยำสูงสุด
- 🚨 ระบบแจ้งเตือน (เสียงและภาพ)
- 📹 บันทึกวิดีโออัตโนมัติเมื่อตรวจพบไฟ
- 📊 แสดงข้อมูล FPS และ Frame count
- 📝 Logging system สำหรับบันทึกเหตุการณ์

## 📋 Requirements

- Python 3.7+
- Webcam/Camera
- OpenCV
- NumPy
- PyTorch (สำหรับ AI detection)
- Ultralytics YOLOv8 (สำหรับ AI detection)

## 🚀 Installation

1. Clone repository:

```bash
git clone https://github.com/KCCHDEV/firede.git
cd firede
```

2. ติดตั้ง dependencies:

```bash
pip install -r requirements.txt
```

**Note**: สำหรับการใช้งาน sound alerts ให้ติดตั้ง pygame:
```bash
pip install pygame
```

## 🎮 Usage

รันโปรแกรม:

```bash
python main.py
```

### Keyboard Controls

- `q` - ออกจากโปรแกรม
- `s` - บันทึกภาพปัจจุบัน

## ⚙️ Configuration

แก้ไขไฟล์ `config.py` เพื่อปรับแต่งการตั้งค่า:

### Camera Settings
- `CAMERA_INDEX`: เลขกล้อง (0 สำหรับกล้องหลัก)
- `CAMERA_WIDTH/HEIGHT`: ขนาดภาพ (default: 640x480)
- `FPS`: Frames per second (default: 30)

### AI Model Settings
- `USE_AI_MODEL`: เปิด/ปิด AI detection (True/False)
- `AI_MODEL_PATH`: Path ไปยัง custom trained model (None = ใช้ pre-trained)
- `AI_CONFIDENCE_THRESHOLD`: ความเชื่อมั่นขั้นต่ำสำหรับ AI (0.0 - 1.0, default: 0.5)
- `USE_HYBRID_MODE`: ใช้ทั้ง AI และ CV (True) หรือ AI เท่านั้น (False)

### Traditional CV Settings
- `FIRE_DETECTION_THRESHOLD`: ความไวในการตรวจจับ (0.0 - 1.0, default: 0.5)
- `MIN_FIRE_AREA`: พื้นที่ขั้นต่ำที่ถือว่าเป็นไฟ (pixels, default: 500)
- `FIRE_CONFIRMATION_FRAMES`: จำนวนเฟรมที่ต้องตรวจพบติดกันเพื่อยืนยัน (default: 3)
- `FIRE_LOWER_HSV`: ค่า HSV ต่ำสุดสำหรับสีไฟ (default: (0, 120, 100))
- `FIRE_UPPER_HSV`: ค่า HSV สูงสุดสำหรับสีไฟ (default: (35, 255, 255))

### Alert & Recording
- `ENABLE_SOUND_ALERT`: เปิด/ปิดเสียงแจ้งเตือน (requires pygame)
- `ALERT_SOUND_PATH`: Path ไปยังไฟล์เสียงแจ้งเตือน (default: "alert.wav")
- `ALERT_COOLDOWN`: ระยะเวลาระหว่างการแจ้งเตือน (วินาที, default: 5)
- `RECORD_ON_DETECTION`: บันทึกวิดีโอเมื่อตรวจพบไฟ (True/False)
- `RECORDING_DURATION`: ระยะเวลาบันทึกหลังตรวจพบไฟ (วินาที, default: 30)
- `OUTPUT_DIR`: โฟลเดอร์บันทึกวิดีโอ (default: "recordings")

### Logging Settings
- `ENABLE_LOGGING`: เปิด/ปิด logging (True/False)
- `LOG_DIR`: โฟลเดอร์บันทึก log files (default: "logs")
- `LOG_LEVEL`: ระดับ logging (DEBUG, INFO, WARNING, ERROR)

### Display Settings
- `SHOW_FPS`: แสดง FPS counter (True/False)
- `SHOW_FRAME_COUNT`: แสดง frame count (True/False)
- `DISPLAY_CONFIDENCE`: แสดง confidence scores (True/False)

## 📁 Project Structure

```
firede/
├── main.py              # Main application
├── fire_detector.py     # Fire detection logic (CV + AI integration)
├── ai_model.py          # AI-based fire detection (YOLOv8)
├── alert.py             # Alert system
├── config.py            # Configuration
├── requirements.txt     # Dependencies
├── recordings/          # Recorded videos (auto-created)
└── logs/                # Log files (auto-created)
```

## 🔧 Technical Details

### Fire Detection Methods

#### AI-based Detection (YOLOv8)
- ใช้ Deep Learning model สำหรับ object detection
- รองรับ GPU acceleration (CUDA) อัตโนมัติ
- สามารถใช้ custom trained model ได้โดยตั้งค่า `AI_MODEL_PATH`
- Confidence threshold ปรับแต่งได้
- ใช้ YOLOv8n (nano) model สำหรับความเร็วสูง

**Note**: Pre-trained YOLOv8 model ไม่ได้ถูกฝึกมาสำหรับตรวจจับไฟโดยเฉพาะ สำหรับการใช้งานจริงแนะนำให้ train custom model ด้วย fire dataset แล้วตั้งค่า `AI_MODEL_PATH` ให้ชี้ไปยัง model ที่ train เอง

#### Traditional Computer Vision
1. **Color-based Detection**: ใช้ HSV color space เพื่อตรวจจับสีไฟ (ส้ม-แดง)
   - Lower HSV: (0, 120, 100) - Red/Orange hues
   - Upper HSV: (35, 255, 255)
   
2. **Morphological Operations**: ลด noise ด้วย opening และ closing
   - Elliptical kernel 5x5
   - 2 iterations each
   
3. **Contour Analysis**: หา contours และกรองตามพื้นที่
   - Minimum area: 500 pixels (configurable)
   - Aspect ratio validation: 0.2 - 5.0
   
4. **Intensity Analysis**: วิเคราะห์ความสว่างเพื่อลด false positives
   - Threshold at 200 for brightness
   - Combines color and brightness masks
   
5. **Motion Analysis**: ตรวจสอบ flickering pattern
   - Frame differencing
   - Motion score threshold: 5
   
6. **Confirmation System**: ต้องตรวจพบติดกันหลายเฟรมเพื่อยืนยัน
   - Default: 3 consecutive frames

#### Hybrid Mode
- รวมผลลัพธ์จาก AI และ CV
- ตรวจพบไฟหากมี**อย่างน้อยหนึ่ง**วิธีตรวจพบ (OR logic)
- เพิ่มความแม่นยำและลด false positives
- ใช้ confidence scores จาก AI เมื่อมี

### Performance

- Real-time processing at 30 FPS (depends on hardware)
- FPS monitoring and display
- Optimized for low latency
- GPU acceleration support (when available)

### Alert System

- Visual alerts: Red border + pulsing text overlay
- Sound alerts: WAV file playback or generated beep
- Cooldown system to prevent alert spam (5 seconds default)
- Threading for non-blocking audio playback

### Recording System

- Automatic recording when fire detected
- MP4 format with configurable duration
- Continues recording while fire is detected
- Stops after configured duration when no fire

## 📝 Notes

- ระบบจะสร้างโฟลเดอร์ `recordings/` และ `logs/` อัตโนมัติ
- วิดีโอจะถูกบันทึกเป็นไฟล์ MP4 ในโฟลเดอร์ `recordings/`
- Log files จะถูกบันทึกในโฟลเดอร์ `logs/` พร้อม timestamp
- สำหรับ alert sound ให้วางไฟล์ `alert.wav` ในโฟลเดอร์หลัก (optional - จะสร้าง beep อัตโนมัติถ้าไม่มีไฟล์)
- การใช้ AI detection ต้องการ GPU แนะนำสำหรับ performance ที่ดี (แต่สามารถใช้ CPU ได้)

## 🐛 Troubleshooting

### กล้องไม่เปิด

- ตรวจสอบว่า CAMERA_INDEX ถูกต้อง
- ลองเปลี่ยนเป็น 1, 2, ... ถ้ามีหลายกล้อง
- ตรวจสอบว่าไม่มีโปรแกรมอื่นใช้กล้องอยู่
- บน Linux: ตรวจสอบว่า user มี permission เข้าถึงกล้อง (`/dev/video0`)

### ตรวจจับผิดพลาด (False Positives)

**ถ้าตรวจจับบ่อยเกินไป:**
- เพิ่ม `MIN_FIRE_AREA` (เช่น จาก 500 เป็น 1000)
- เพิ่ม `FIRE_CONFIRMATION_FRAMES` (เช่น จาก 3 เป็น 5)
- ลด `FIRE_DETECTION_THRESHOLD` (เช่น จาก 0.5 เป็น 0.3)
- ปรับค่า `FIRE_LOWER_HSV` และ `FIRE_UPPER_HSV` ให้แคบลง

**ถ้าตรวจจับไม่ได้:**
- ลด `MIN_FIRE_AREA` (เช่น จาก 500 เป็น 300)
- ลด `FIRE_CONFIRMATION_FRAMES` (เช่น จาก 3 เป็น 2)
- เพิ่ม `FIRE_DETECTION_THRESHOLD` (เช่น จาก 0.5 เป็น 0.7)
- ปรับค่า `FIRE_LOWER_HSV` และ `FIRE_UPPER_HSV` ให้กว้างขึ้น

### AI Detection ไม่ทำงาน

- ตรวจสอบว่าติดตั้ง PyTorch และ Ultralytics แล้ว: `pip install torch ultralytics`
- ดูใน logs ว่ามี error message อะไร
- ตรวจสอบว่า GPU drivers ถูกต้อง (สำหรับ CUDA)
- ลอง run ด้วย CPU โดยไม่มี CUDA

### Performance Issues

- ลด `CAMERA_WIDTH` และ `CAMERA_HEIGHT` (เช่น 320x240)
- ลด `FPS` (เช่น 15 หรือ 20)
- ปิด AI detection หรือใช้ CPU-only mode
- ปิด `RECORD_ON_DETECTION` ถ้าไม่จำเป็น
- ตรวจสอบ CPU/GPU usage

### Sound Alert ไม่ทำงาน

- ติดตั้ง pygame: `pip install pygame`
- ตรวจสอบว่ามีไฟล์ `alert.wav` (optional - จะสร้าง beep เอง)
- ตรวจสอบ audio output settings ของระบบ
- ดู logs สำหรับ error messages

### Import Errors

```bash
# ถ้ามี import errors ให้ติดตั้งทั้งหมดใหม่
pip install --upgrade pip
pip install -r requirements.txt
pip install pygame  # Optional for sound
```

## 🎓 Training Custom Model

สำหรับการใช้งานจริง แนะนำให้ train YOLOv8 model ของคุณเองด้วย fire dataset:

1. รวบรวม dataset ของไฟและควัน
2. Annotate ด้วย tools อย่าง [Roboflow](https://roboflow.com/)
3. Train ด้วย Ultralytics YOLOv8:

```python
from ultralytics import YOLO

# Load a model
model = YOLO('yolov8n.pt')

# Train the model
results = model.train(data='fire.yaml', epochs=100, imgsz=640)
```

4. ตั้งค่า `AI_MODEL_PATH` ใน `config.py` ให้ชี้ไปยัง model ที่ train

**Fire Datasets ที่แนะนำ:**
- [Fire Detection Dataset (Roboflow)](https://universe.roboflow.com/fire-detection)
- [Fire and Smoke Dataset (Kaggle)](https://www.kaggle.com/datasets/dataclusterlabs/fire-and-smoke-dataset)

## 🔒 Security Considerations

- ระบบนี้ควรใช้ร่วมกับ fire alarm systems แบบดั้งเดิม ไม่ใช่ทดแทน
- ตรวจสอบและ validate false positives ก่อนการแจ้งเตือนจริง
- ทดสอบระบบในสภาพแวดล้อมที่คล้ายกับการใช้งานจริง
- พิจารณาเพิ่ม notification systems (email, SMS, etc.)

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📄 License

MIT License

## 🙏 Acknowledgments

- [Ultralytics YOLOv8](https://github.com/ultralytics/ultralytics)
- [OpenCV](https://opencv.org/)
- [PyTorch](https://pytorch.org/)

## 📧 Contact

For questions or issues, please open an issue on GitHub.

---

Made with ❤️ by KCCHDEV
