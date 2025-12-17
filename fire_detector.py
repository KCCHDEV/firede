"""
Fire Detector combining Traditional CV and AI approaches
"""
import cv2
import numpy as np
import logging
from typing import Tuple, List, Optional
from collections import deque

import config
from ai_model import AIFireDetector


class FireDetector:
    """Fire detection using Computer Vision and AI"""
    
    def __init__(self):
        """Initialize fire detector"""
        self.frame_count = 0
        self.fire_frames = deque(maxlen=config.FIRE_CONFIRMATION_FRAMES)
        self.prev_gray = None
        
        # Initialize AI detector if enabled
        self.ai_detector = None
        if config.USE_AI_MODEL:
            try:
                self.ai_detector = AIFireDetector(
                    model_path=config.AI_MODEL_PATH,
                    confidence_threshold=config.AI_CONFIDENCE_THRESHOLD
                )
                if self.ai_detector.is_available():
                    logging.info("AI detection initialized successfully")
                else:
                    logging.warning("AI detection not available, using CV only")
                    self.ai_detector = None
            except Exception as e:
                logging.error(f"Failed to initialize AI detector: {e}")
                self.ai_detector = None
    
    def detect_fire_cv(self, frame: np.ndarray) -> Tuple[bool, List[Tuple[int, int, int, int]]]:
        """
        Detect fire using traditional Computer Vision techniques
        
        Args:
            frame: Input frame (BGR format)
        
        Returns:
            Tuple of (fire_detected, bounding_boxes)
        """
        # Convert to HSV color space
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        
        # Create mask for fire color range
        lower_hsv = np.array(config.FIRE_LOWER_HSV)
        upper_hsv = np.array(config.FIRE_UPPER_HSV)
        mask = cv2.inRange(hsv, lower_hsv, upper_hsv)
        
        # Morphological operations to reduce noise
        kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))
        mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel, iterations=2)
        mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel, iterations=2)
        
        # Additional intensity check for bright regions
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        _, bright_mask = cv2.threshold(gray, 200, 255, cv2.THRESH_BINARY)
        
        # Combine color and brightness masks
        combined_mask = cv2.bitwise_and(mask, bright_mask)
        
        # Find contours
        contours, _ = cv2.findContours(combined_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
        fire_boxes = []
        fire_detected = False
        
        for contour in contours:
            area = cv2.contourArea(contour)
            
            # Filter by minimum area
            if area >= config.MIN_FIRE_AREA:
                x, y, w, h = cv2.boundingRect(contour)
                
                # Additional validation: check aspect ratio
                aspect_ratio = float(w) / h if h > 0 else 0
                if 0.2 < aspect_ratio < 5.0:  # Reasonable aspect ratio
                    fire_boxes.append((x, y, x + w, y + h))
                    fire_detected = True
        
        # Motion/flicker analysis
        if fire_detected and self.prev_gray is not None:
            curr_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            frame_diff = cv2.absdiff(self.prev_gray, curr_gray)
            motion_score = np.mean(frame_diff)
            
            # Fire typically has motion/flicker
            if motion_score < 5:  # Too static, might be false positive
                fire_detected = False
                fire_boxes = []
        
        self.prev_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        
        return fire_detected, fire_boxes
    
    def detect_fire_ai(self, frame: np.ndarray) -> Tuple[bool, List[Tuple[int, int, int, int]], List[float]]:
        """
        Detect fire using AI model
        
        Args:
            frame: Input frame (BGR format)
        
        Returns:
            Tuple of (fire_detected, bounding_boxes, confidence_scores)
        """
        if self.ai_detector is None or not self.ai_detector.is_available():
            return False, [], []
        
        return self.ai_detector.detect(frame)
    
    def detect(self, frame: np.ndarray) -> Tuple[bool, List[Tuple[int, int, int, int]], List[float], str]:
        """
        Main detection method that combines AI and CV approaches
        
        Args:
            frame: Input frame (BGR format)
        
        Returns:
            Tuple of (fire_detected, bounding_boxes, confidence_scores, detection_method)
            - fire_detected: Boolean indicating if fire was detected
            - bounding_boxes: List of (x1, y1, x2, y2) coordinates
            - confidence_scores: List of confidence scores (empty for CV detection)
            - detection_method: String indicating which method detected fire ('AI', 'CV', 'Hybrid', 'None')
        """
        self.frame_count += 1
        
        cv_detected = False
        cv_boxes = []
        ai_detected = False
        ai_boxes = []
        ai_confidences = []
        
        # Run CV detection if hybrid mode or AI not available
        if config.USE_HYBRID_MODE or self.ai_detector is None:
            cv_detected, cv_boxes = self.detect_fire_cv(frame)
        
        # Run AI detection if available
        if self.ai_detector is not None and self.ai_detector.is_available():
            ai_detected, ai_boxes, ai_confidences = self.detect_fire_ai(frame)
        
        # Determine final result based on mode
        if config.USE_HYBRID_MODE and self.ai_detector is not None:
            # Hybrid mode: fire detected if EITHER method detects it
            fire_detected = cv_detected or ai_detected
            
            # Combine boxes from both methods
            all_boxes = cv_boxes + ai_boxes
            
            # For hybrid, we prioritize AI confidences
            if ai_detected:
                detection_method = "Hybrid (AI+CV)"
                final_confidences = ai_confidences
            elif cv_detected:
                detection_method = "Hybrid (CV)"
                final_confidences = [config.FIRE_DETECTION_THRESHOLD] * len(cv_boxes)
            else:
                detection_method = "None"
                final_confidences = []
        elif self.ai_detector is not None and self.ai_detector.is_available():
            # AI only mode
            fire_detected = ai_detected
            all_boxes = ai_boxes
            final_confidences = ai_confidences
            detection_method = "AI" if ai_detected else "None"
        else:
            # CV only mode (fallback)
            fire_detected = cv_detected
            all_boxes = cv_boxes
            final_confidences = [config.FIRE_DETECTION_THRESHOLD] * len(cv_boxes)
            detection_method = "CV" if cv_detected else "None"
        
        # Confirmation system: need detection in multiple consecutive frames
        self.fire_frames.append(fire_detected)
        confirmed_fire = sum(self.fire_frames) >= config.FIRE_CONFIRMATION_FRAMES
        
        if not confirmed_fire:
            return False, [], [], "None"
        
        return confirmed_fire, all_boxes, final_confidences, detection_method
    
    def reset(self):
        """Reset detector state"""
        self.fire_frames.clear()
        self.prev_gray = None
