# ==========================================================
# ZeusShopBot PRO
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
    "https://t.me/Vpn1_v2rayNG"
)



# ==========================================================
# 3X-UI PANEL
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


# API TOKEN
PANEL_TOKEN = os.getenv(
    "PANEL_TOKEN",
    ""
)



# Inbound ID

INBOUND_ID = int(
    os.getenv(
        "INBOUND_ID",
        "1"
    )
)



# ==========================================================
# Payment
# ==========================================================

CARD_NUMBER = os.getenv(
    "CARD_NUMBER",
    "0000-0000-0000-0000"
)


CARD_HOLDER = os.getenv(
    "CARD_HOLDER",
    "صاحب کارت"
)


BANK_NAME = os.getenv(
    "BANK_NAME",
    "بانک"
)



# ==========================================================
# Plans
# ==========================================================


PLANS = {


    "plan_basic": {

        "name": "⚡ اقتصادی",

        "traffic": "20GB",

        "gb": 20,

        "days": 15,

        "price": 120000

    },


    "plan_silver": {

        "name": "🔥 نقره‌ای",

        "traffic": "50GB",

        "gb": 50,

        "days": 30,

        "price": 250000

    },


    "plan_gold": {

        "name": "💎 طلایی",

        "traffic": "100GB",

        "gb": 100,

        "days": 30,

        "price": 400000

    },


    "plan_vip": {

        "name": "👑 VIP",

        "traffic": "Unlimited",

        "gb": 0,

        "days": 30,

        "price": 600000

    },


    "custom": {

        "name": "🛠 حجم دلخواه",

        "traffic": "Custom",

        "gb": 0,

        "days": 30,

        "price": 0

    }


}



# قیمت هر گیگ

PRICE_PER_GB = 6000
