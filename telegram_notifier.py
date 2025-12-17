"""
Telegram Notification System for Fire Detection
"""
import logging
import time
from threading import Thread
from typing import Optional
import requests

import config


class TelegramNotifier:
    """Telegram notification system for fire alerts"""
    
    def __init__(self):
        """Initialize Telegram notifier"""
        self.enabled = config.TELEGRAM_ENABLED
        self.bot_token = config.TELEGRAM_BOT_TOKEN
        self.chat_id = config.TELEGRAM_CHAT_ID
        self.last_notification_time = 0
        self.notification_cooldown = 30  # Minimum seconds between notifications
        
        if self.enabled:
            # Test connection
            if self._test_connection():
                logging.info("Telegram notifications enabled and ready")
            else:
                logging.warning("Telegram connection test failed. Notifications disabled.")
                self.enabled = False
    
    def _test_connection(self) -> bool:
        """Test Telegram bot connection"""
        try:
            url = f"https://api.telegram.org/bot{self.bot_token}/getMe"
            response = requests.get(url, timeout=5)
            if response.status_code == 200:
                return True
            else:
                logging.error(f"Telegram bot test failed: {response.status_code}")
                return False
        except Exception as e:
            logging.error(f"Failed to connect to Telegram: {e}")
            return False
    
    def send_message(self, message: str) -> bool:
        """
        Send text message to Telegram
        
        Args:
            message: Message text to send
        
        Returns:
            True if sent successfully
        """
        if not self.enabled:
            return False
        
        # Check cooldown
        current_time = time.time()
        if current_time - self.last_notification_time < self.notification_cooldown:
            logging.debug("Telegram notification skipped (cooldown)")
            return False
        
        try:
            url = f"https://api.telegram.org/bot{self.bot_token}/sendMessage"
            payload = {
                'chat_id': self.chat_id,
                'text': message,
                'parse_mode': 'HTML'
            }
            
            response = requests.post(url, json=payload, timeout=10)
            
            if response.status_code == 200:
                self.last_notification_time = current_time
                logging.info("Telegram notification sent successfully")
                return True
            else:
                logging.error(f"Failed to send Telegram message: {response.status_code}")
                return False
                
        except Exception as e:
            logging.error(f"Error sending Telegram message: {e}")
            return False
    
    def send_photo(self, photo_path: str, caption: str = "") -> bool:
        """
        Send photo to Telegram
        
        Args:
            photo_path: Path to photo file
            caption: Optional caption for the photo
        
        Returns:
            True if sent successfully
        """
        if not self.enabled:
            return False
        
        try:
            url = f"https://api.telegram.org/bot{self.bot_token}/sendPhoto"
            
            with open(photo_path, 'rb') as photo_file:
                files = {'photo': photo_file}
                data = {
                    'chat_id': self.chat_id,
                    'caption': caption,
                    'parse_mode': 'HTML'
                }
                
                response = requests.post(url, data=data, files=files, timeout=30)
            
            if response.status_code == 200:
                logging.info("Telegram photo sent successfully")
                return True
            else:
                logging.error(f"Failed to send Telegram photo: {response.status_code}")
                return False
                
        except Exception as e:
            logging.error(f"Error sending Telegram photo: {e}")
            return False
    
    def send_fire_alert(self, detection_method: str = "Unknown") -> None:
        """
        Send fire detection alert to Telegram (non-blocking)
        
        Args:
            detection_method: Method that detected the fire
        """
        if not self.enabled:
            return
        
        def send_alert():
            message = (
                "🚨 <b>FIRE ALERT!</b> 🚨\n\n"
                f"Fire detected using <b>{detection_method}</b> method\n"
                f"Time: {time.strftime('%Y-%m-%d %H:%M:%S')}\n\n"
                "Please check the camera feed immediately!"
            )
            self.send_message(message)
        
        # Send in background thread
        thread = Thread(target=send_alert, daemon=True)
        thread.start()
    
    def send_fire_photo(self, photo_path: str, detection_method: str = "Unknown") -> None:
        """
        Send fire detection photo to Telegram (non-blocking)
        
        Args:
            photo_path: Path to the fire detection screenshot
            detection_method: Method that detected the fire
        """
        if not self.enabled:
            return
        
        def send_photo_alert():
            caption = (
                f"🔥 Fire detected via {detection_method}\n"
                f"Time: {time.strftime('%Y-%m-%d %H:%M:%S')}"
            )
            self.send_photo(photo_path, caption)
        
        # Send in background thread
        thread = Thread(target=send_photo_alert, daemon=True)
        thread.start()
