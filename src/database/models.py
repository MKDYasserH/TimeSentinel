class ActivityLog:
    def __init__(self, window_title, start_time, end_time):
        self.window_title = window_title
        self.start_time = start_time
        self.end_time = end_time

    def duration(self):
        return self.end_time - self.start_time


class UserSettings:
    def __init__(self, forbidden_apps=None):
        if forbidden_apps is None:
            forbidden_apps = []
        self.forbidden_apps = forbidden_apps

    def add_forbidden_app(self, app_name):
        if app_name not in self.forbidden_apps:
            self.forbidden_apps.append(app_name)

    def remove_forbidden_app(self, app_name):
        if app_name in self.forbidden_apps:
            self.forbidden_apps.remove(app_name)