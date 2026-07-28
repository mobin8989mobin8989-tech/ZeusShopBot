# ==========================================================
# ZeusShopBot
# modules/database.py
# ==========================================================

import sqlite3
from pathlib import Path


DATABASE_FILE = Path("zeus.db")


class Database:

    def __init__(self):
        self.connection = None

    def connect(self):
        self.connection = sqlite3.connect(DATABASE_FILE)
        self.connection.row_factory = sqlite3.Row
        return self.connection

    def cursor(self):
        if self.connection is None:
            self.connect()
        return self.connection.cursor()

    def commit(self):
        if self.connection:
            self.connection.commit()

    def close(self):
        if self.connection:
            self.connection.close()
            self.connection = None


db = Database()
