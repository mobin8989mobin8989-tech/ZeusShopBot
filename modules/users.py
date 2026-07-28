# ==========================================================
# ZeusShopBot PRO
# modules/users.py
# ==========================================================

import sqlite3


DB_NAME = "zeus.db"



# ==========================================================
# Database Connection
# ==========================================================

def get_db():

    return sqlite3.connect(DB_NAME)



# ==========================================================
# Create Tables
# ==========================================================

def init_db():

    db = get_db()

    cursor = db.cursor()


    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (

        id INTEGER PRIMARY KEY AUTOINCREMENT,

        telegram_id INTEGER UNIQUE,

        username TEXT,

        first_name TEXT,

        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP

    )
    """)


    db.commit()

    db.close()





# ==========================================================
# Users Manager
# ==========================================================

class Users:


    def __init__(self):

        init_db()



    # ==========================
    # Add User
    # ==========================

    def add_user(

        self,

        telegram_id,

        username=None,

        first_name=None

    ):


        db = get_db()

        cursor = db.cursor()



        cursor.execute("""

        INSERT OR IGNORE INTO users

        (

        telegram_id,

        username,

        first_name

        )

        VALUES (?,?,?)

        """,

        (

        telegram_id,

        username,

        first_name

        ))



        db.commit()

        db.close()





    # ==========================
    # Get Users
    # ==========================

    def get_users(self):


        db = get_db()

        cursor = db.cursor()


        cursor.execute(

            "SELECT * FROM users"

        )


        users = cursor.fetchall()


        db.close()


        return users





# ==========================================================
# Export
# ==========================================================

users = Users()
