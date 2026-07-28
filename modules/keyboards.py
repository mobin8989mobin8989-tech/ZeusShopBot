# ==========================================================
# ZeusShopBot PRO
# modules/keyboards.py
# ==========================================================

from telegram import (
    InlineKeyboardButton,
    InlineKeyboardMarkup
)



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
                callback_data="buy_service"
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
                "🧾 سفارش‌ها",
                callback_data="orders"
            )
        ],


        [
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
# Plans Menu
# ==========================================================

def plans_menu():


    keyboard = [

        [

            InlineKeyboardButton(
                "⚡ اقتصادی | 20GB | 15 روز",
                callback_data="plan_basic"
            )

        ],


        [

            InlineKeyboardButton(
                "🔥 نقره‌ای | 50GB | 30 روز",
                callback_data="plan_silver"
            )

        ],


        [

            InlineKeyboardButton(
                "💎 طلایی | 100GB | 30 روز",
                callback_data="plan_gold"
            )

        ],


        [

            InlineKeyboardButton(
                "👑 VIP نامحدود",
                callback_data="plan_vip"
            )

        ],


        [

            InlineKeyboardButton(
                "🛠 حجم دلخواه",
                callback_data="custom"
            )

        ],


        [

            InlineKeyboardButton(
                "⬅ بازگشت",
                callback_data="main_menu"
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
                "📢 پیام همگانی",
                callback_data="admin_broadcast"
            ),

            InlineKeyboardButton(
                "🎟 تخفیف‌ها",
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


    return InlineKeyboardMarkup(

        [

            [

                InlineKeyboardButton(
                    "⬅ بازگشت",
                    callback_data="main_menu"
                )

            ]

        ]

    )





# ==========================================================
# Confirm Button
# ==========================================================

def confirm_menu():


    return InlineKeyboardMarkup(

        [

            [

                InlineKeyboardButton(
                    "✅ تایید",
                    callback_data="confirm"
                ),


                InlineKeyboardButton(
                    "❌ لغو",
                    callback_data="cancel"
                )

            ]

        ]

    )
