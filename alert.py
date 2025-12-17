"""
Alert System for Fire Detection
"""
import os
import time
import logging
from threading import Thread
import numpy as np

try:
    import pygame
    PYGAME_AVAILABLE = True
except ImportError:
    PYGAME_AVAILABLE = False
    logging.warning("pygame not available. Sound alerts will be disabled.")

import config


class AlertSystem:
    """Alert system for fire detection notifications"""
    
    def __init__(self):
        """Initialize alert system"""
        self.last_alert_time = 0
        self.alert_active = False
        self.sound_initialized = False
        
        # Initialize pygame mixer for sound
        if config.ENABLE_SOUND_ALERT and PYGAME_AVAILABLE:
            try:
                pygame.mixer.init()
                self.sound_initialized = True
                logging.info("Sound alert system initialized")
            except Exception as e:
                logging.error(f"Failed to initialize pygame mixer: {e}")
                self.sound_initialized = False
    
    def play_sound_alert(self):
        """Play alert sound in a separate thread"""
        if not self.sound_initialized or not config.ENABLE_SOUND_ALERT:
            return
        
        def play_sound():
            try:
                if os.path.exists(config.ALERT_SOUND_PATH):
                    sound = pygame.mixer.Sound(config.ALERT_SOUND_PATH)
                    sound.play()
                    logging.info("Playing alert sound")
                else:
                    # Generate beep sound if file doesn't exist
                    logging.warning(f"Alert sound file not found: {config.ALERT_SOUND_PATH}")
                    # Create a simple beep using numpy and pygame
                    self._generate_beep()
            except Exception as e:
                logging.error(f"Error playing sound: {e}")
        
        thread = Thread(target=play_sound, daemon=True)
        thread.start()
    
    def _generate_beep(self):
        """Generate a simple beep sound"""
        try:
            sample_rate = 22050
            duration = 0.5  # seconds
            frequency = 1000  # Hz
            
            # Generate sine wave
            samples = int(sample_rate * duration)
            t = np.linspace(0, duration, samples)
            wave = np.sin(2 * np.pi * frequency * t)
            
            # Convert to 16-bit integer
            wave = (wave * 32767).astype(np.int16)
            
            # Create stereo sound
            stereo_wave = np.column_stack((wave, wave))
            
            # Create pygame sound
            sound = pygame.sndarray.make_sound(stereo_wave)
            sound.play()
            logging.info("Playing generated beep sound")
        except Exception as e:
            logging.error(f"Error generating beep: {e}")
    
    def trigger_alert(self):
        """Trigger fire alert"""
        current_time = time.time()
        
        # Check cooldown to avoid spam
        if current_time - self.last_alert_time < config.ALERT_COOLDOWN:
            return
        
        self.last_alert_time = current_time
        self.alert_active = True
        
        # Play sound alert
        self.play_sound_alert()
        
        # Log alert
        logging.warning("🚨 FIRE DETECTED! Alert triggered.")
    
    def clear_alert(self):
        """Clear alert state"""
        self.alert_active = False
    
    def draw_alert_overlay(self, frame: np.ndarray) -> np.ndarray:
        """
        Draw alert overlay on frame
        
        Args:
            frame: Input frame
        
        Returns:
            Frame with alert overlay
        """
        if not self.alert_active:
            return frame
        
        # Create a copy to draw on
        overlay = frame.copy()
        
        # Draw red border
        height, width = frame.shape[:2]
        border_thickness = 10
        import cv2
        cv2.rectangle(overlay, (0, 0), (width, height), (0, 0, 255), border_thickness)
        
        # Draw alert text
        alert_text = "🔥 FIRE DETECTED! 🔥"
        font = cv2.FONT_HERSHEY_BOLD
        font_scale = 1.5
        thickness = 3
        
        # Get text size
        (text_width, text_height), _ = cv2.getTextSize(alert_text, font, font_scale, thickness)
        
        # Position text at top center
        text_x = (width - text_width) // 2
        text_y = 50
        
        # Draw text background
        padding = 10
        cv2.rectangle(overlay, 
                     (text_x - padding, text_y - text_height - padding),
                     (text_x + text_width + padding, text_y + padding),
                     (0, 0, 255), -1)
        
        # Draw text
        cv2.putText(overlay, alert_text, (text_x, text_y), font, 
                   font_scale, (255, 255, 255), thickness)
        
        # Blend overlay with original frame for pulsing effect
        alpha = 0.7 + 0.3 * abs(time.time() % 1 - 0.5) * 2  # Pulsing effect
        result = cv2.addWeighted(overlay, alpha, frame, 1 - alpha, 0)
        
        return result
    
    def cleanup(self):
        """Cleanup alert system resources"""
        if self.sound_initialized and PYGAME_AVAILABLE:
            try:
                pygame.mixer.quit()
            except Exception as e:
                logging.error(f"Error during alert system cleanup: {e}")
