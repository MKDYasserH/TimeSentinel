from pynput import mouse, keyboard
from typing import Dict
from datetime import datetime
import threading

class InputTracker:
    def __init__(self):
        self.stats = {
            'mouse_clicks': 0,
            'keystrokes': 0,
            'last_activity': datetime.now()
        }
        self._lock = threading.Lock()

    def on_click(self, x, y, button, pressed):
        """Mouse click callback."""
        if pressed:
            with self._lock:
                self.stats['mouse_clicks'] += 1
                self.stats['last_activity'] = datetime.now()

    def on_press(self, key):
        """Keyboard press callback."""
        with self._lock:
            self.stats['keystrokes'] += 1
            self.stats['last_activity'] = datetime.now()

    def start_tracking(self):
        """Start tracking mouse and keyboard inputs."""
        mouse_listener = mouse.Listener(on_click=self.on_click)
        keyboard_listener = keyboard.Listener(on_press=self.on_press)
        
        mouse_listener.start()
        keyboard_listener.start()
        
        return mouse_listener, keyboard_listener

    def get_stats(self) -> Dict:
        """Get current input statistics."""
        with self._lock:
            return self.stats.copy()

    def reset_stats(self):
        """Reset all statistics."""
        with self._lock:
            self.stats = {
                'mouse_clicks': 0,
                'keystrokes': 0,
                'last_activity': datetime.now()
            }