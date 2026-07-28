# ==========================================================
# Zeus Shop VPN PRO
# config.py
# ==========================================================

import os

# =========================
# Telegram
# =========================

BOT_TOKEN = os.getenv("BOT_TOKEN", "")
ADMIN_ID = int(os.getenv("ADMIN_ID", "0"))
CHANNEL = os.getenv("CHANNEL", "@ZeusShop")

# =========================
# 3X-UI Panel
# =========================

PANEL_URL = os.getenv("PANEL_URL", "")
PANEL_USERNAME = os.getenv("PANEL_USERNAME", "")
PANEL_PASSWORD = os.getenv("PANEL_PASSWORD", "")
INBOUND_ID = int(os.getenv("INBOUND_ID", "1"))

# =========================
# Payment
# =========================

CARD_NUMBER = os.getenv("CARD_NUMBER", "")
CARD_HOLDER = os.getenv("CARD_HOLDER", "")
BANK_NAME = os.getenv("BANK_NAME", "")

# =========================
# Database
# =========================

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///zeus.db")

# =========================
# Plans
# =========================

PRICE_PER_GB = int(os.getenv("PRICE_PER_GB", "3500"))

PLANS = {
    "plan_20": {
        "name": "⚡ اقتصادی",
        "price": 70000,
        "days": 15,
        "traffic": "20GB"
    },
    "plan_50": {
        "name": "🔥 نقره‌ای",
        "price": 175000,
        "days": 30,
        "traffic": "50GB"
    },
    "plan_100": {
        "name": "💎 طلایی",
        "price": 350000,
        "days": 30,
        "traffic": "100GB"
    },
    "plan_unlimited": {
        "name": "👑 VIP",
        "price": 650000,
        "days": 30,
        "traffic": "نامحدود"
    },
    "custom": {
        "name": "🛠 حجم دلخواه",
        "price": 0,
        "days": 30,
        "traffic": "Custom"
    }
}
