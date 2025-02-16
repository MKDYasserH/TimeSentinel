import json
from datetime import datetime, timedelta
from pathlib import Path
import os

class StreakManager:
    def __init__(self):
        self.current_streak = 0
        self.streak_minutes = 0
        self.last_check = datetime.now()
        self.blocked_apps = set()
        self.blocked_domains = set()
        self.load_blocked_items()
        
    def load_blocked_items(self):
        """Load blocked items from configuration files."""
        config_dir = Path(__file__).resolve().parent.parent.parent / 'config'
        
        # Load default blocks
        with open(config_dir / 'default_blocks.json', 'r') as f:
            defaults = json.load(f)
            self.default_apps = set(defaults.get('apps', []))
            self.default_domains = set(defaults.get('domains', []))
        
        # Load custom blocks
        custom_path = config_dir / 'blocked_items.json'
        if custom_path.exists():
            with open(custom_path, 'r') as f:
                custom = json.load(f)
                self.blocked_apps = self.default_apps | set(custom.get('apps', []))
                self.blocked_domains = self.default_domains | set(custom.get('domains', []))
        else:
            self.blocked_apps = self.default_apps
            self.blocked_domains = self.default_domains
    
    def save_blocked_items(self):
        """Save custom blocked items to configuration file."""
        config_dir = Path(__file__).resolve().parent.parent.parent / 'config'
        custom_blocks = {
            'apps': list(self.blocked_apps - self.default_apps),
            'domains': list(self.blocked_domains - self.default_domains)
        }
        with open(config_dir / 'blocked_items.json', 'w') as f:
            json.dump(custom_blocks, f, indent=2)

    def is_default_blocked(self, item, item_type):
        """Check if an item is in the default blocked list."""
        if item_type == 'apps':
            return item in self.default_apps
        return item in self.default_domains

    def check_blocked(self, window_info, browser_info):
        """Check if current window/domain is blocked."""
        app_name = window_info.get('app_name', '')
        if app_name in self.blocked_apps:
            return True
        
        if browser_info and browser_info.get('domain') in self.blocked_domains:
            return True
        
        return False

    def update_streak(self, is_blocked):
        """Update streak based on current activity."""
        now = datetime.now()
        time_diff = now - self.last_check
        
        if is_blocked:
            # Reset streak if blocked content is accessed
            self.current_streak = 0
            self.streak_minutes = 0
        else:
            # Only update if less than 5 minutes have passed since last check
            if time_diff <= timedelta(minutes=5):
                minutes = time_diff.total_seconds() / 60
                self.streak_minutes += minutes
                
                # Convert minutes to hours and update streak
                while self.streak_minutes >= 60:
                    self.current_streak += 1
                    self.streak_minutes -= 60
            else:
                # Reset streak if more than 5 minutes have passed
                self.current_streak = 0
                self.streak_minutes = 0
        
        self.last_check = now

    def format_streak(self):
        """Format the streak for display."""
        if self.current_streak == 0 and self.streak_minutes < 1:
            return {
                'main': "No active streak",
                'detail': "Start focusing to build your streak!"
            }
        
        hours = self.current_streak
        minutes = int(self.streak_minutes)
        
        if hours == 0:
            main = f"{minutes} minutes"
        elif hours == 1:
            main = f"1 hour {minutes} minutes"
        else:
            main = f"{hours} hours {minutes} minutes"
        
        detail = "Keep going! Stay focused to increase your streak."
        
        return {
            'main': main,
            'detail': detail
        }

    def add_blocked_app(self, app):
        """Add an app to blocked list."""
        self.blocked_apps.add(app)
        self.save_blocked_items()

    def remove_blocked_app(self, app):
        """Remove an app from blocked list if it's not a default."""
        if app not in self.default_apps:
            self.blocked_apps.remove(app)
            self.save_blocked_items()

    def add_blocked_domain(self, domain):
        """Add a domain to blocked list."""
        self.blocked_domains.add(domain)
        self.save_blocked_items()

    def remove_blocked_domain(self, domain):
        """Remove a domain from blocked list if it's not a default."""
        if domain not in self.default_domains:
            self.blocked_domains.remove(domain)
            self.save_blocked_items()