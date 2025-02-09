class DatabaseManager:
    def __init__(self, db_path):
        import sqlite3
        self.connection = sqlite3.connect(db_path)
        self.cursor = self.connection.cursor()
        self.create_tables()

    def create_tables(self):
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS activity_logs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                window_title TEXT NOT NULL,
                duration INTEGER NOT NULL,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        self.connection.commit()

    def add_activity_log(self, window_title, duration):
        self.cursor.execute('''
            INSERT INTO activity_logs (window_title, duration)
            VALUES (?, ?)
        ''', (window_title, duration))
        self.connection.commit()

    def get_activity_logs(self):
        self.cursor.execute('SELECT * FROM activity_logs')
        return self.cursor.fetchall()

    def close(self):
        self.connection.close()