from typing import Dict, Optional, Callable
from datetime import datetime
from .window_tracker import WindowTracker
from .input_tracker import InputTracker
from .browser_tracker import BrowserTracker
import threading
from rewards.streak_manager import StreakManager

class ActivityTracker:
    def __init__(self):
        self.window_tracker = WindowTracker()
        self.input_tracker = InputTracker()
        self.browser_tracker = BrowserTracker()
        self.running = False
        self.callback: Optional[Callable] = None
        self.tracking_thread: Optional[threading.Thread] = None
        self._stop_event = threading.Event()  # New stop event
        self.streak_manager = StreakManager()

    def window_change_callback(self, window_info: Dict, duration: float):
        """Callback for window changes."""
        stats = self.input_tracker.get_stats()
        
        # Add browser URL tracking
        browser_info = {}
        if window_info['app_name'] in ['Google Chrome', 'Safari']:
            current_url = self.browser_tracker.get_current_url(window_info['app_name'])
            if (current_url):
                browser_info = {
                    'url': current_url,
                    'domain': self.browser_tracker.get_domain(current_url)
                }

        # Check if current window/domain is blocked
        is_blocked = self.streak_manager.check_blocked(window_info, browser_info)
        self.streak_manager.update_streak(is_blocked)

        activity_data = {
            'window_info': window_info,
            'browser_info': browser_info,  # Add browser info to the log
            'duration': duration,
            'mouse_clicks': stats['mouse_clicks'],
            'keystrokes': stats['keystrokes'],
            'timestamp': datetime.now(),
            'is_blocked': is_blocked,
            'current_streak': self.streak_manager.current_streak
        }
        
        if self.callback:
            self.callback(activity_data)
        
        # Reset input stats for new window
        self.input_tracker.reset_stats()

    def _run_tracking(self):
        # New wrapper method: pass the stop event so the window tracker loop can exit
        self.window_tracker.track_windows(self.window_change_callback, self._stop_event)

    def start(self, callback: Optional[Callable] = None):
        """Start tracking all activity."""
        self.callback = callback
        self.running = True
        self._stop_event.clear()  # Clear any previous stop signals
        
        # Start input tracking
        self.input_tracker.start_tracking()
        
        # Start window tracking in a separate thread
        self.tracking_thread = threading.Thread(
            target=self._run_tracking
        )
        self.tracking_thread.daemon = True
        self.tracking_thread.start()

    def stop(self):
        """Stop tracking activity."""
        self.running = False
        if hasattr(self.window_tracker, "stop_tracking"):
            self.window_tracker.stop_tracking()
        if hasattr(self.input_tracker, "stop_tracking"):
            self.input_tracker.stop_tracking()
        self._stop_event.set()  # Signal the window tracking loop to exit
        if self.tracking_thread:
            self.tracking_thread.join(timeout=2)