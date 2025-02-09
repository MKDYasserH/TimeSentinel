class StreakManager:
    def __init__(self):
        self.current_streak = 0
        self.last_session_end = None
        self.forbidden_apps = set()

    def start_session(self):
        self.last_session_end = None

    def end_session(self):
        self.last_session_end = self.get_current_time()

    def increment_streak(self):
        self.current_streak += 1

    def reset_streak(self):
        self.current_streak = 0

    def check_forbidden(self, active_window):
        return active_window in self.forbidden_apps

    def get_current_time(self):
        from datetime import datetime
        return datetime.now()