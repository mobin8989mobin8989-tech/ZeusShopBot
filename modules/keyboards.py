# ==========================================================
# ZeusShopBot PRO
# modules/keyboards.py
# ==========================================================

from telegram import InlineKeyboardButton, InlineKeyboardMarkup


# ==========================================================
# Main Menu
# ==========================================================

def main_menu():

    keyboard = [

        [
            InlineKeyboardButton(
                "🛒 خرید سرویس",
                callback_data="buy_service"
            )
        ],

        [
            InlineKeyboardButton(
                "🌍 سرویس‌های من",
                callback_data="my_services"
            ),

            InlineKeyboardButton(
                "👤 حساب کاربری",
                callback_data="profile"
            )
        ],

        [
            InlineKeyboardButton(
                "💎 پلن‌ها",
                callback_data="plans"
            ),

            InlineKeyboardButton(
                "🎁 کد تخفیف",
                callback_data="discount"
            )
        ],

        [
            InlineKeyboardButton(
                "💰 کیف پول",
                callback_data="wallet"
            ),

            InlineKeyboardButton(
                "🧾 سفارش‌های من",
                callback_data="orders"
            )
        ],

        [
            InlineKeyboardButton(
                "📈 وضعیت مصرف",
                callback_data="usage"
            ),

            InlineKeyboardButton(
                "🔄 تمدید سرویس",
                callback_data="renew"
            )
        ],

        [
            InlineKeyboardButton(
                "🎧 پشتیبانی",
                callback_data="support"
            ),

            InlineKeyboardButton(
                "📚 آموزش اتصال",
                callback_data="tutorial"
            )
        ],

        [
            InlineKeyboardButton(
                "📢 کانال اطلاع‌رسانی",
                url="https://t.me/Vpn1_v2rayNG"
            )
        ]

    ]

    return InlineKeyboardMarkup(keyboard)


# ==========================================================
# Admin Menu
# ==========================================================

def admin_menu():

    keyboard = [

        [
            InlineKeyboardButton(
                "👥 کاربران",
                callback_data="admin_users"
            ),

            InlineKeyboardButton(
                "📦 سفارشات",
                callback_data="admin_orders"
            )
        ],

        [
            InlineKeyboardButton(
                "💳 پرداخت‌ها",
                callback_data="admin_payments"
            ),

            InlineKeyboardButton(
                "📡 سرویس‌ها",
                callback_data="admin_services"
            )
        ],

        [
            InlineKeyboardButton(
                "📢 ارسال همگانی",
                callback_data="admin_broadcast"
            ),

            InlineKeyboardButton(
                "🎟 کد تخفیف",
                callback_data="admin_discount"
            )
        ],

        [
            InlineKeyboardButton(
                "📊 آمار",
                callback_data="admin_stats"
            ),

            InlineKeyboardButton(
                "⚙ تنظیمات",
                callback_data="admin_settings"
            )
        ]

    ]

    return InlineKeyboardMarkup(keyboard)


# ==========================================================
# Back Button
# ==========================================================

def back_menu():

    keyboard = [

        [

            InlineKeyboardButton(
                "⬅ بازگشت",
                callback_data="main_menu"
            )

        ]

    ]

    return InlineKeyboardMarkup(keyboard)


# ==========================================================
# Confirm Menu
# ==========================================================

def confirm_menu():

    keyboard = [

        [

            InlineKeyboardButton(
                "✅ تایید",
                callback_data="confirm"
            ),

            InlineKeyboardButton(
                "❌ انصراف",
                callback_data="cancel"
            )

        ]

    ]

    return InlineKeyboardMarkup(keyboard)
