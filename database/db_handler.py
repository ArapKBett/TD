import sqlite3
import contextlib
from datetime import datetime
from config.settings import Config

class Database:
    def __init__(self):
        self.conn = sqlite3.connect(Config.DB_PATH)
        self._create_tables()

    def _create_tables(self):
        with self.conn:
            self.conn.execute('''
                CREATE TABLE IF NOT EXISTS security_data (
                    id INTEGER PRIMARY KEY,
                    source TEXT NOT NULL,
                    category TEXT NOT NULL,
                    title TEXT NOT NULL,
                    description TEXT,
                    code_sample TEXT,
                    severity TEXT,
                    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                    verified BOOLEAN DEFAULT 0
                )''')
            
            self.conn.execute('''
                CREATE TABLE IF NOT EXISTS users (
                    user_id INTEGER PRIMARY KEY,
                    access_level INTEGER DEFAULT 1,
                    last_request DATETIME
                )''')

    @contextlib.contextmanager
    def cursor(self):
        cursor = self.conn.cursor()
        try:
            yield cursor
        finally:
            cursor.close()

    def log_request(self, user_id):
        with self.cursor() as c:
            c.execute('''
                INSERT OR REPLACE INTO users (user_id, last_request)
                VALUES (?, ?)
            ''', (user_id, datetime.now()))
            self.conn.commit()
