# ==========================================================
# ZeusShopBot
# modules/payments.py
# ==========================================================

from modules.database import db


class PaymentManager:

    def create_table(self):

        conn = db.connect()
        cursor = conn.cursor()

        cursor.execute("""
        CREATE TABLE IF NOT EXISTS payments (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            telegram_id INTEGER,
            plan TEXT,
            amount INTEGER,
            receipt_file_id TEXT,
            status TEXT DEFAULT 'pending',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """)

        db.commit()

    def create_payment(
        self,
        telegram_id,
        plan,
        amount,
        receipt_file_id=None
    ):

        conn = db.connect()
        cursor = conn.cursor()

        cursor.execute("""
        INSERT INTO payments
        (
            telegram_id,
            plan,
            amount,
            receipt_file_id,
            status
        )
        VALUES (?, ?, ?, ?, ?)
        """, (
            telegram_id,
            plan,
            amount,
            receipt_file_id,
            "pending"
        ))

        db.commit()

        return cursor.lastrowid

    def get_payment(
        self,
        payment_id
    ):

        conn = db.connect()
        cursor = conn.cursor()

        cursor.execute(
            "SELECT * FROM payments WHERE id=?",
            (payment_id,)
        )

        return cursor.fetchone()

    def update_status(
        self,
        payment_id,
        status
    ):

        conn = db.connect()
        cursor = conn.cursor()

        cursor.execute(
            "UPDATE payments SET status=? WHERE id=?",
            (status, payment_id)
        )

        db.commit()

    def pending_payments(self):

        conn = db.connect()
        cursor = conn.cursor()

        cursor.execute(
            "SELECT * FROM payments WHERE status='pending'"
        )

        return cursor.fetchall()

    def approved_payments(self):

        conn = db.connect()
        cursor = conn.cursor()

        cursor.execute(
            "SELECT * FROM payments WHERE status='approved'"
        )

        return cursor.fetchall()


payments = PaymentManager()
