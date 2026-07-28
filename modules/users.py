# ==========================================================
# ZeusShopBot
# modules/users.py
# ==========================================================

from modules.database import db


class UserManager:

    def create_table(self):

        conn = db.connect()
        cursor = conn.cursor()

        cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            telegram_id INTEGER UNIQUE,
            username TEXT,
            first_name TEXT,
            balance INTEGER DEFAULT 0,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """)

        db.commit()

    def add_user(
        self,
        telegram_id,
        username,
        first_name
    ):

        conn = db.connect()
        cursor = conn.cursor()

        cursor.execute("""
        INSERT OR IGNORE INTO users
        (
            telegram_id,
            username,
            first_name
        )
        VALUES (?, ?, ?)
        """, (
            telegram_id,
            username,
            first_name
        ))

        db.commit()

    def get_user(
        self,
        telegram_id
    ):

        conn = db.connect()
        cursor = conn.cursor()

        cursor.execute(
            "SELECT * FROM users WHERE telegram_id=?",
            (telegram_id,)
        )

        return cursor.fetchone()

    def get_all_users(self):

        conn = db.connect()
        cursor = conn.cursor()

        cursor.execute(
            "SELECT * FROM users"
        )

        return cursor.fetchall()

    def count_users(self):

        conn = db.connect()
        cursor = conn.cursor()

        cursor.execute(
            "SELECT COUNT(*) FROM users"
        )

        return cursor.fetchone()[0]


users = UserManager()
