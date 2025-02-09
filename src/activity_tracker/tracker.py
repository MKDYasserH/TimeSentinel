from typing import Dict, Optional, Callable
from datetime import datetime
from .window_tracker import WindowTracker
from .input_tracker import InputTracker
from .browser_tracker import BrowserTracker
import threading

class ActivityTracker:
    def __init__(self):
        self.window_tracker = WindowTracker()
        self.input_tracker = InputTracker()
        self.browser_tracker = BrowserTracker()
        self.running = False
        self.callback: Optional[Callable] = None

    def window_change_callback(self, window_info: Dict, duration: float):
        """Callback for window changes."""
        stats = self.input_tracker.get_stats()
        
        # Add browser URL tracking
        browser_info = {}
        if window_info['app_name'] in ['Google Chrome', 'Safari']:
            current_url = self.browser_tracker.get_current_url(window_info['app_name'])
            if current_url:
                browser_info = {
                    'url': current_url,
                    'domain': self.browser_tracker.get_domain(current_url)
                }

        activity_data = {
            'window_info': window_info,
            'browser_info': browser_info,  # Add browser info to the log
            'duration': duration,
            'mouse_clicks': stats['mouse_clicks'],
            'keystrokes': stats['keystrokes'],
            'timestamp': datetime.now()
        }
        
        if self.callback:
            self.callback(activity_data)
        
        # Reset input stats for new window
        self.input_tracker.reset_stats()

    def start(self, callback: Optional[Callable] = None):
        """Start tracking all activity."""
        self.callback = callback
        self.running = True
        
        # Start input tracking
        self.input_tracker.start_tracking()
        
        # Start window tracking in a separate thread
        tracking_thread = threading.Thread(
            target=self.window_tracker.track_windows,
            args=(self.window_change_callback,)
        )
        tracking_thread.daemon = True
        tracking_thread.start()

    def stop(self):
        """Stop tracking activity."""
        self.running = False