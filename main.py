"""
Fire Detection System - Main Application
Real-time fire detection using Computer Vision and AI
"""
import cv2
import os
import sys
import time
import logging
from datetime import datetime
from pathlib import Path

import config
from fire_detector import FireDetector
from alert import AlertSystem


class FireDetectionSystem:
    """Main Fire Detection System"""
    
    def __init__(self):
        """Initialize fire detection system"""
        # Setup logging
        self._setup_logging()
        
        # Create necessary directories
        self._create_directories()
        
        # Initialize components
        self.detector = FireDetector()
        self.alert_system = AlertSystem()
        
        # Camera
        self.camera = None
        self.camera_opened = False
        
        # Recording
        self.video_writer = None
        self.recording = False
        self.recording_start_time = 0
        
        # Stats
        self.frame_count = 0
        self.fps = 0
        self.last_fps_time = time.time()
        self.fps_frame_count = 0
        
        logging.info("Fire Detection System initialized")
    
    def _setup_logging(self):
        """Setup logging configuration"""
        if config.ENABLE_LOGGING:
            log_dir = Path(config.LOG_DIR)
            log_dir.mkdir(exist_ok=True)
            
            log_file = log_dir / f"fire_detection_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"
            
            logging.basicConfig(
                level=getattr(logging, config.LOG_LEVEL),
                format='%(asctime)s - %(levelname)s - %(message)s',
                handlers=[
                    logging.FileHandler(log_file),
                    logging.StreamHandler(sys.stdout)
                ]
            )
            logging.info(f"Logging to: {log_file}")
    
    def _create_directories(self):
        """Create necessary directories"""
        Path(config.OUTPUT_DIR).mkdir(exist_ok=True)
        if config.ENABLE_LOGGING:
            Path(config.LOG_DIR).mkdir(exist_ok=True)
        logging.info("Directories created")
    
    def open_camera(self) -> bool:
        """
        Open camera device
        
        Returns:
            True if camera opened successfully
        """
        try:
            self.camera = cv2.VideoCapture(config.CAMERA_INDEX)
            
            if not self.camera.isOpened():
                logging.error(f"Failed to open camera {config.CAMERA_INDEX}")
                return False
            
            # Set camera properties
            self.camera.set(cv2.CAP_PROP_FRAME_WIDTH, config.CAMERA_WIDTH)
            self.camera.set(cv2.CAP_PROP_FRAME_HEIGHT, config.CAMERA_HEIGHT)
            self.camera.set(cv2.CAP_PROP_FPS, config.FPS)
            
            # Verify settings
            actual_width = int(self.camera.get(cv2.CAP_PROP_FRAME_WIDTH))
            actual_height = int(self.camera.get(cv2.CAP_PROP_FRAME_HEIGHT))
            actual_fps = int(self.camera.get(cv2.CAP_PROP_FPS))
            
            logging.info(f"Camera opened: {actual_width}x{actual_height} @ {actual_fps} FPS")
            self.camera_opened = True
            return True
            
        except Exception as e:
            logging.error(f"Error opening camera: {e}")
            return False
    
    def start_recording(self, frame):
        """Start video recording"""
        if not config.RECORD_ON_DETECTION or self.recording:
            return
        
        try:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            filename = os.path.join(config.OUTPUT_DIR, f"fire_{timestamp}.{config.OUTPUT_FORMAT}")
            
            # Define codec and create VideoWriter
            fourcc = cv2.VideoWriter_fourcc(*'mp4v')
            height, width = frame.shape[:2]
            
            self.video_writer = cv2.VideoWriter(
                filename,
                fourcc,
                config.FPS,
                (width, height)
            )
            
            if self.video_writer.isOpened():
                self.recording = True
                self.recording_start_time = time.time()
                logging.info(f"Started recording: {filename}")
            else:
                logging.error("Failed to start video recording")
                
        except Exception as e:
            logging.error(f"Error starting recording: {e}")
    
    def stop_recording(self):
        """Stop video recording"""
        if self.recording and self.video_writer is not None:
            self.video_writer.release()
            self.video_writer = None
            self.recording = False
            logging.info("Stopped recording")
    
    def update_fps(self):
        """Update FPS calculation"""
        self.fps_frame_count += 1
        current_time = time.time()
        elapsed = current_time - self.last_fps_time
        
        if elapsed >= 1.0:  # Update every second
            self.fps = self.fps_frame_count / elapsed
            self.fps_frame_count = 0
            self.last_fps_time = current_time
    
    def draw_info(self, frame, fire_detected, boxes, confidences, detection_method):
        """Draw information overlays on frame"""
        height, width = frame.shape[:2]
        
        # Draw bounding boxes
        for i, (x1, y1, x2, y2) in enumerate(boxes):
            color = (0, 0, 255)  # Red for fire
            cv2.rectangle(frame, (x1, y1), (x2, y2), color, 2)
            
            # Draw confidence score if available
            if config.DISPLAY_CONFIDENCE and i < len(confidences):
                conf_text = f"{confidences[i]:.2f}"
                cv2.putText(frame, conf_text, (x1, y1 - 10),
                           cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)
        
        # Draw FPS
        if config.SHOW_FPS:
            fps_text = f"FPS: {self.fps:.1f}"
            cv2.putText(frame, fps_text, (10, 30),
                       cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
        
        # Draw frame count
        if config.SHOW_FRAME_COUNT:
            frame_text = f"Frame: {self.frame_count}"
            cv2.putText(frame, frame_text, (10, 60),
                       cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
        
        # Draw detection method
        if fire_detected:
            method_text = f"Method: {detection_method}"
            cv2.putText(frame, method_text, (10, 90),
                       cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 255), 2)
        
        # Draw recording indicator
        if self.recording:
            rec_text = "● REC"
            cv2.putText(frame, rec_text, (width - 100, 30),
                       cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
        
        return frame
    
    def run(self):
        """Main run loop"""
        if not self.open_camera():
            logging.error("Cannot start system: Camera not available")
            return
        
        logging.info("Fire Detection System started")
        logging.info("Press 'q' to quit, 's' to save screenshot")
        
        try:
            while True:
                # Read frame
                ret, frame = self.camera.read()
                if not ret:
                    logging.error("Failed to read frame from camera")
                    break
                
                self.frame_count += 1
                self.update_fps()
                
                # Detect fire
                fire_detected, boxes, confidences, detection_method = self.detector.detect(frame)
                
                # Handle fire detection
                if fire_detected:
                    self.alert_system.trigger_alert()
                    
                    # Start recording if not already recording
                    if not self.recording:
                        self.start_recording(frame)
                    
                    logging.info(f"Fire detected (Method: {detection_method})")
                else:
                    self.alert_system.clear_alert()
                
                # Handle recording duration
                if self.recording:
                    elapsed = time.time() - self.recording_start_time
                    if elapsed >= config.RECORDING_DURATION and not fire_detected:
                        self.stop_recording()
                    elif self.video_writer is not None:
                        self.video_writer.write(frame)
                
                # Draw information overlays
                display_frame = self.draw_info(frame, fire_detected, boxes, 
                                              confidences, detection_method)
                
                # Draw alert overlay
                display_frame = self.alert_system.draw_alert_overlay(display_frame)
                
                # Show frame
                cv2.imshow('Fire Detection System', display_frame)
                
                # Handle keyboard input
                key = cv2.waitKey(1) & 0xFF
                
                if key == ord('q'):
                    logging.info("Quit requested by user")
                    break
                elif key == ord('s'):
                    # Save screenshot
                    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
                    filename = os.path.join(config.OUTPUT_DIR, f"screenshot_{timestamp}.jpg")
                    cv2.imwrite(filename, frame)
                    logging.info(f"Screenshot saved: {filename}")
                    
        except KeyboardInterrupt:
            logging.info("Interrupted by user")
        except Exception as e:
            logging.error(f"Error in main loop: {e}", exc_info=True)
        finally:
            self.cleanup()
    
    def cleanup(self):
        """Cleanup resources"""
        logging.info("Cleaning up...")
        
        # Stop recording
        self.stop_recording()
        
        # Release camera
        if self.camera is not None:
            self.camera.release()
        
        # Close windows
        cv2.destroyAllWindows()
        
        # Cleanup alert system
        self.alert_system.cleanup()
        
        logging.info("Cleanup complete")


def main():
    """Main entry point"""
    print("=" * 60)
    print("🔥 Fire Detection System")
    print("=" * 60)
    print(f"AI Detection: {'Enabled' if config.USE_AI_MODEL else 'Disabled'}")
    print(f"Hybrid Mode: {'Enabled' if config.USE_HYBRID_MODE else 'Disabled'}")
    print(f"Camera: {config.CAMERA_INDEX}")
    print(f"Resolution: {config.CAMERA_WIDTH}x{config.CAMERA_HEIGHT}")
    print("=" * 60)
    print()
    
    system = FireDetectionSystem()
    system.run()


if __name__ == "__main__":
    main()
