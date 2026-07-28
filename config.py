# ==========================================================
# Zeus Shop VPN PRO
# config.py
# ==========================================================

import os


# ==========================================================
# Telegram
# ==========================================================

BOT_TOKEN = os.getenv(
    "BOT_TOKEN",
    ""
)


ADMIN_ID = int(
    os.getenv(
        "ADMIN_ID",
        "0"
    )
)


CHANNEL = os.getenv(
    "CHANNEL",
    "@ZeusShop"
)



# ==========================================================
# 3X-UI Panel
# ==========================================================

PANEL_URL = os.getenv(
    "PANEL_URL",
    ""
)


PANEL_USERNAME = os.getenv(
    "PANEL_USERNAME",
    ""
)


PANEL_PASSWORD = os.getenv(
    "PANEL_PASSWORD",
    ""
)


# Inbound شماره 4 پنل شما
INBOUND_ID = int(
    os.getenv(
        "INBOUND_ID",
        "4"
    )
)



# ==========================================================
# Payment
# ==========================================================

CARD_NUMBER = os.getenv(
    "CARD_NUMBER",
    ""
)


CARD_HOLDER = os.getenv(
    "CARD_HOLDER",
    ""
)


BANK_NAME = os.getenv(
    "BANK_NAME",
    ""
)



# ==========================================================
# Database
# ==========================================================

DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "sqlite:///zeus.db"
)



# ==========================================================
# Pricing
# ==========================================================

# قیمت هر گیگابایت
PRICE_PER_GB = int(
    os.getenv(
        "PRICE_PER_GB",
        "6000"
    )
)



# ==========================================================
# Plans
# ==========================================================

PLANS = {


    # 20 گیگ
    "plan_20": {

        "name": "⚡ پلن اقتصادی",

        "price": 120000,

        "days": 15,

        "traffic": "20GB"

    },


    # 50 گیگ
    "plan_50": {

        "name": "🔥 پلن نقره‌ای",

        "price": 300000,

        "days": 30,

        "traffic": "50GB"

    },


    # 100 گیگ
    "plan_100": {

        "name": "💎 پلن طلایی",

        "price": 600000,

        "days": 30,

        "traffic": "100GB"

    },


    # نامحدود
    "plan_unlimited": {

        "name": "👑 پلن VIP",

        "price": 900000,

        "days": 30,

        "traffic": "نامحدود"

    },


    # حجم دلخواه
    "custom": {

        "name": "🛠 حجم دلخواه",

        "price": 0,

        "days": 30,

        "traffic": "Custom"

    }

}
