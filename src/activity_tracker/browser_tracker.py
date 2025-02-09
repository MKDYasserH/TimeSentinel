import os
import sqlite3
from typing import Optional
from urllib.parse import urlparse
import time

class BrowserTracker:
    def __init__(self):
        self.chrome_history_path = os.path.expanduser(
            "~/Library/Application Support/Google/Chrome/Default/History"
        )
        self.safari_history_path = os.path.expanduser(
            "~/Library/Safari/History.db"
        )

    def get_current_url(self, browser_name: str) -> Optional[str]:
        """Get the most recent URL from browser history."""
        if browser_name.lower() == "google chrome":
            return self._get_chrome_url()
        elif browser_name.lower() == "safari":
            return self._get_safari_url()
        return None

    def _get_chrome_url(self) -> Optional[str]:
        try:
            # Create a copy of the database since Chrome locks it
            tmp_path = "/tmp/chrome_history_tmp"
            os.system(f"cp '{self.chrome_history_path}' '{tmp_path}'")
            
            conn = sqlite3.connect(tmp_path)
            cursor = conn.cursor()
            
            # Get the most recent URL
            cursor.execute("""
                SELECT url FROM urls 
                ORDER BY last_visit_time DESC 
                LIMIT 1
            """)
            
            result = cursor.fetchone()
            conn.close()
            os.remove(tmp_path)
            
            return result[0] if result else None
        except Exception:
            return None

    def _get_safari_url(self) -> Optional[str]:
        try:
            conn = sqlite3.connect(self.safari_history_path)
            cursor = conn.cursor()
            
            cursor.execute("""
                SELECT url FROM history_items 
                ORDER BY visit_time DESC 
                LIMIT 1
            """)
            
            result = cursor.fetchone()
            conn.close()
            
            return result[0] if result else None
        except Exception:
            return None

    def get_domain(self, url: str) -> Optional[str]:
        """Extract domain from URL."""
        try:
            return urlparse(url).netloc
        except Exception:
            return None