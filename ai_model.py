"""
AI-based Fire Detection using YOLOv8
"""
import os
import logging
from typing import Tuple, List, Optional
import numpy as np

try:
    from ultralytics import YOLO
    import torch
    YOLO_AVAILABLE = True
except ImportError:
    YOLO_AVAILABLE = False
    logging.warning("Ultralytics YOLO not available. AI detection will be disabled.")


class AIFireDetector:
    """AI-based fire detector using YOLOv8"""
    
    def __init__(self, model_path: Optional[str] = None, confidence_threshold: float = 0.5):
        """
        Initialize AI fire detector
        
        Args:
            model_path: Path to custom trained model. If None, uses pre-trained YOLOv8
            confidence_threshold: Minimum confidence score (0.0 - 1.0)
        """
        self.model = None
        self.confidence_threshold = confidence_threshold
        self.device = 'cuda' if torch.cuda.is_available() else 'cpu'
        
        if not YOLO_AVAILABLE:
            logging.warning("YOLO not available. AI detection disabled.")
            return
        
        try:
            if model_path and os.path.exists(model_path):
                # Load custom trained model
                self.model = YOLO(model_path)
                logging.info(f"Loaded custom model from {model_path}")
            else:
                # Load pre-trained YOLOv8 model (auto-downloads if not present)
                # First time run will download ~6MB yolov8n.pt model automatically
                logging.info("Loading YOLOv8 model (will auto-download if needed)...")
                self.model = YOLO('yolov8n.pt')  # Nano version for speed
                logging.info("YOLOv8 model loaded successfully")
            
            self.model.to(self.device)
            logging.info(f"Model running on: {self.device}")
            
        except Exception as e:
            logging.error(f"Failed to load YOLO model: {e}")
            self.model = None
    
    def detect(self, frame: np.ndarray) -> Tuple[bool, List[Tuple[int, int, int, int]], List[float]]:
        """
        Detect fire in frame using AI
        
        Args:
            frame: Input frame (BGR format)
        
        Returns:
            Tuple of (fire_detected, bounding_boxes, confidence_scores)
            - fire_detected: Boolean indicating if fire was detected
            - bounding_boxes: List of (x1, y1, x2, y2) coordinates
            - confidence_scores: List of confidence scores for each detection
        """
        if self.model is None or not YOLO_AVAILABLE:
            return False, [], []
        
        try:
            # Run inference
            results = self.model(frame, verbose=False)
            
            fire_boxes = []
            fire_confidences = []
            
            for result in results:
                boxes = result.boxes
                for box in boxes:
                    # Get class name
                    class_id = int(box.cls[0])
                    class_name = result.names[class_id].lower()
                    confidence = float(box.conf[0])
                    
                    # ⚠️ IMPORTANT: Standard YOLOv8 pre-trained models (yolov8n.pt) do NOT
                    # have fire detection classes. This code is designed for CUSTOM TRAINED models.
                    # 
                    # To use AI detection effectively:
                    # 1. Train a custom YOLOv8 model with fire/smoke/flame classes
                    # 2. Set AI_MODEL_PATH in config.py to your custom model path
                    # 3. The model will then detect fire using the trained classes
                    # 
                    # Until you have a custom model, it's recommended to:
                    # - Set USE_AI_MODEL = False in config.py
                    # - Use CV-only detection (which works out of the box)
                    
                    if confidence >= self.confidence_threshold:
                        # Check if class name contains fire-related keywords
                        # This will only work with custom trained models that have these classes
                        fire_keywords = ['fire', 'smoke', 'flame']
                        if any(keyword in class_name.lower() for keyword in fire_keywords):
                            x1, y1, x2, y2 = box.xyxy[0].cpu().numpy().astype(int)
                            fire_boxes.append((x1, y1, x2, y2))
                            fire_confidences.append(confidence)
                            logging.info(f"AI detected fire: class='{class_name}', confidence={confidence:.2f}")
            
            fire_detected = len(fire_boxes) > 0
            return fire_detected, fire_boxes, fire_confidences
            
        except Exception as e:
            logging.error(f"Error during AI detection: {e}")
            return False, [], []
    
    def is_available(self) -> bool:
        """Check if AI model is available and ready"""
        return self.model is not None and YOLO_AVAILABLE
