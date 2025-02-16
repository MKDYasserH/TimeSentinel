from typing import Dict, Optional
import Quartz
from datetime import datetime
import time

class WindowTracker:
    def __init__(self):
        self.current_window: Dict = {}
        self.last_window_switch: datetime = datetime.now()

    def start_tracking(self):
        # Start tracking the active window
        pass

    def stop_tracking(self):
        # Stop tracking the active window
        pass

    def get_active_window_info(self) -> Optional[Dict]:
        """Get information about the currently active window."""
        window_list = Quartz.CGWindowListCopyWindowInfo(
            Quartz.kCGWindowListOptionOnScreenOnly | Quartz.kCGWindowListExcludeDesktopElements,
            Quartz.kCGNullWindowID
        )
        
        for window in window_list:
            if window.get(Quartz.kCGWindowLayer, 0) == 0:  # Active window is at layer 0
                return {
                    'app_name': window.get(Quartz.kCGWindowOwnerName, ''),
                    'window_title': window.get(Quartz.kCGWindowName, ''),
                    'timestamp': datetime.now()
                }
        return None

    def track_windows(self, callback=None, stop_event=None):
        """Continuously track window changes."""
        try:
            while True:
                if stop_event is not None and stop_event.is_set():
                    break
                current_window = self.get_active_window_info()
                
                if current_window and current_window != self.current_window:
                    if self.current_window:
                        duration = (datetime.now() - self.last_window_switch).total_seconds()
                        if callback:
                            callback(self.current_window, duration)
                    
                    self.current_window = current_window
                    self.last_window_switch = current_window['timestamp']
                
                time.sleep(1)  # Check every second
        except KeyboardInterrupt:
            pass
        finally:
            if self.current_window and callback:
                duration = (datetime.now() - self.last_window_switch).total_seconds()
                callback(self.current_window, duration)