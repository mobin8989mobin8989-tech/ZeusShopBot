# ==========================================================
# Zeus Shop VPN PRO
# handlers.py
# Part 1
# ==========================================================

from telegram import (
    Update,
    InlineKeyboardButton,
    InlineKeyboardMarkup
)

from telegram.ext import (
    ContextTypes,
    CommandHandler,
    CallbackQueryHandler,
    MessageHandler,
    filters
)

from modules.keyboards import *
from modules.users import users
from modules.orders import OrderManager
from modules.payments import payments
from modules.support import support
from modules.plans import plans

from config import (
    ADMIN_ID,
    CHANNEL
)


# ==========================================================
# Welcome Text
# ==========================================================

WELCOME_TEXT = f"""
╔══════════════════════╗
        👑 Zeus Shop VPN
╚══════════════════════╝

🚀 به فروشگاه هوشمند Zeus Shop خوش آمدید.

با استفاده از Zeus Shop همیشه به اینترنتی سریع، پایدار و بدون محدودیت متصل خواهید بود.

━━━━━━━━━━━━━━━━━━━━━━

⚡ تحویل آنی سرویس

🛡 امنیت و پایداری بالا

🌍 سرورهای پرسرعت

📡 مناسب تمامی اپراتورها

🎁 تخفیف‌های ویژه کاربران

💬 پشتیبانی همه روزه

━━━━━━━━━━━━━━━━━━━━━━

📢 قبل از خرید لطفاً عضو کانال اطلاع‌رسانی شوید:

{CHANNEL}

👇 از منوی زیر گزینه موردنظر خود را انتخاب کنید.
"""


# ==========================================================
# /start
# ==========================================================

async def start(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    user = update.effective_user

    users.add_user(
        telegram_id=user.id,
        username=user.username,
        first_name=user.first_name
    )

    await update.message.reply_text(
        text=WELCOME_TEXT,
        reply_markup=main_menu()
    )
    # ==========================================================
# Zeus Shop VPN PRO
# handlers.py
# Part 2
# ==========================================================

from telegram import InlineKeyboardButton, InlineKeyboardMarkup


# ==========================================================
# Buy Menu
# ==========================================================

BUY_TEXT = """
🛒 خرید اشتراک VPN

یکی از پلن‌های زیر را انتخاب کنید.

━━━━━━━━━━━━━━━━━━

⚡ اقتصادی
20GB | 15 روز

🔥 نقره‌ای
50GB | 30 روز

💎 طلایی
100GB | 30 روز

👑 VIP
نامحدود | 30 روز

🛠 حجم دلخواه
انتخاب حجم توسط شما

━━━━━━━━━━━━━━━━━━

لطفاً یکی از گزینه‌ها را انتخاب کنید.
"""


def plans_menu():

    keyboard = [

        [
            InlineKeyboardButton(
                "⚡ 20GB",
                callback_data="plan_20"
            ),

            InlineKeyboardButton(
                "🔥 50GB",
                callback_data="plan_50"
            )

        ],

        [

            InlineKeyboardButton(
                "💎 100GB",
                callback_data="plan_100"
            ),

            InlineKeyboardButton(
                "👑 نامحدود",
                callback_data="plan_unlimited"
            )

        ],

        [

            InlineKeyboardButton(
                "🛠 حجم دلخواه",
                callback_data="plan_custom"
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
# Buy Service
# ==========================================================

async def buy_service(

    update: Update,

    context: ContextTypes.DEFAULT_TYPE

):

    query = update.callback_query

    await query.answer()

    await query.edit_message_text(

        BUY_TEXT,

        reply_markup=plans_menu()

    )
    # ==========================================================
# Zeus Shop VPN PRO
# handlers.py
# Part 3
# ==========================================================

from config import PLANS


# ==========================================================
# Select Plan
# ==========================================================

async def select_plan(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    query = update.callback_query

    await query.answer()

    plan_key = query.data

    if plan_key not in PLANS:

        return

    plan = PLANS[plan_key]

    # ======================================================
    # حجم دلخواه
    # ======================================================

    if plan_key == "custom":

        context.user_data["waiting_custom_gb"] = True

        await query.edit_message_text(
            "🛠 حجم دلخواه\n\n"
            "لطفاً مقدار حجم موردنظر خود را به گیگابایت وارد کنید.\n\n"
            "💰 قیمت هر گیگ: ۳۵۰۰ تومان\n\n"
            "مثال:\n"
            "`75`",
            parse_mode="Markdown"
        )

        return

    # ======================================================
    # ذخیره پلن
    # ======================================================

    context.user_data["selected_plan"] = plan_key

    text = f"""
✅ پلن انتخاب شد

📦 {plan["name"]}

🌐 حجم:
{plan["traffic"]}

📅 مدت:
{plan["days"]} روز

💰 مبلغ:
{plan["price"]:,} تومان

━━━━━━━━━━━━━━━━━━

برای ادامه پرداخت روی دکمه زیر کلیک کنید.
"""

    keyboard = InlineKeyboardMarkup(

        [

            [

                InlineKeyboardButton(
                    "💳 پرداخت",
                    callback_data="payment"
                )

            ],

            [

                InlineKeyboardButton(
                    "⬅ بازگشت",
                    callback_data="buy_service"
                )

            ]

        ]

    )

    await query.edit_message_text(

        text,

        reply_markup=keyboard

    )


# ==========================================================
# Custom Volume
# ==========================================================

async def custom_volume(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    if not context.user_data.get("waiting_custom_gb"):

        return

    try:

        gb = int(update.message.text)

    except:

        await update.message.reply_text(
            "❌ فقط عدد وارد کنید."
        )

        return

    if gb < 5:

        await update.message.reply_text(
            "❌ حداقل حجم 5 گیگ است."
        )

        return

    price = gb * 3500

    context.user_data["waiting_custom_gb"] = False

    context.user_data["custom_gb"] = gb

    context.user_data["custom_price"] = price

    keyboard = InlineKeyboardMarkup(

        [

            [

                InlineKeyboardButton(
                    "💳 پرداخت",
                    callback_data="payment_custom"
                )

            ],

            [

                InlineKeyboardButton(
                    "⬅ بازگشت",
                    callback_data="buy_service"
                )

            ]

        ]

    )

    await update.message.reply_text(

        f"""✅ حجم دلخواه ثبت شد

🌐 حجم:
{gb} GB

💰 مبلغ:
{price:,} تومان

برای ادامه پرداخت روی دکمه زیر کلیک کنید.""",

        reply_markup=keyboard

        )
   # ==========================================================
# Zeus Shop VPN PRO
# handlers.py
# Part 4
# Payment System
# ==========================================================

from config import (
    CARD_NUMBER,
    CARD_HOLDER
)

# ==========================================================
# Payment Page
# ==========================================================

async def payment(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    query = update.callback_query

    await query.answer()

    if "custom_price" in context.user_data:

        price = context.user_data["custom_price"]

        traffic = f'{context.user_data["custom_gb"]} GB'

        days = 30

    else:

        plan = PLANS[
            context.user_data["selected_plan"]
        ]

        price = plan["price"]

        traffic = plan["traffic"]

        days = plan["days"]

    context.user_data["waiting_receipt"] = True

    keyboard = InlineKeyboardMarkup(

        [

            [

                InlineKeyboardButton(
                    "📤 ارسال رسید",
                    callback_data="send_receipt"
                )

            ],

            [

                InlineKeyboardButton(
                    "⬅ بازگشت",
                    callback_data="buy_service"
                )

            ]

        ]

    )

    text = f"""
💳 اطلاعات پرداخت

━━━━━━━━━━━━━━━━━━

💰 مبلغ:

{price:,} تومان

🌐 حجم:

{traffic}

📅 مدت:

{days} روز

━━━━━━━━━━━━━━━━━━

🏦 شماره کارت

`{CARD_NUMBER}`

👤 صاحب حساب

{CARD_HOLDER}

━━━━━━━━━━━━━━━━━━

پس از پرداخت روی
📤 ارسال رسید
کلیک کنید.
"""

    await query.edit_message_text(
        text,
        parse_mode="Markdown",
        reply_markup=keyboard
    )


# ==========================================================
# Send Receipt
# ==========================================================

async def send_receipt(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    query = update.callback_query

    await query.answer()

    await query.message.reply_text(

        "📷 لطفاً تصویر رسید پرداخت را ارسال کنید."

    )


# ==========================================================
# Receive Receipt
# ==========================================================

async def receipt_handler(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    if not context.user_data.get("waiting_receipt"):

        return

    if not update.message.photo:

        await update.message.reply_text(

            "❌ لطفاً تصویر ارسال کنید."

        )

        return

    file_id = update.message.photo[-1].file_id

    context.user_data["receipt"] = file_id

    context.user_data["waiting_receipt"] = False

    await update.message.reply_text(

        "✅ رسید شما دریافت شد.\n\n"
        "پس از تأیید ادمین، سرویس به صورت خودکار ساخته خواهد شد."

        )
# ==========================================================
# Zeus Shop VPN PRO
# handlers.py
# Part 5
# ==========================================================

from telegram import InlineKeyboardButton
from telegram import InlineKeyboardMarkup

from modules.panel import Panel

panel = Panel()


# ==========================================================
# Send Receipt To Admin
# ==========================================================

async def send_receipt_to_admin(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    photo = context.user_data["receipt"]

    user = update.effective_user

    if "custom_price" in context.user_data:

        price = context.user_data["custom_price"]

        traffic = f"{context.user_data['custom_gb']} GB"

        days = 30

    else:

        plan = PLANS[
            context.user_data["selected_plan"]
        ]

        price = plan["price"]

        traffic = plan["traffic"]

        days = plan["days"]

    keyboard = InlineKeyboardMarkup(

        [

            [

                InlineKeyboardButton(

                    "✅ تایید",

                    callback_data=f"approve_{user.id}"

                ),

                InlineKeyboardButton(

                    "❌ رد",

                    callback_data=f"reject_{user.id}"

                )

            ]

        ]

    )

    await context.bot.send_photo(

        chat_id=ADMIN_ID,

        photo=photo,

        caption=f"""

💳 پرداخت جدید

━━━━━━━━━━━━━━

👤 کاربر

{user.first_name}

🆔

{user.id}

🌐 حجم

{traffic}

📅 مدت

{days} روز

💰 مبلغ

{price:,} تومان

""",

        reply_markup=keyboard

    )


# ==========================================================
# Approve Payment
# ==========================================================

async def approve_payment(

    update: Update,

    context: ContextTypes.DEFAULT_TYPE

):

    query = update.callback_query

    await query.answer()

    user_id = int(

        query.data.split("_")[1]

    )

    try:

        service = panel.create_service(

            user_id=user_id

        )

        await context.bot.send_message(

            chat_id=user_id,

            text=f"""

🎉 پرداخت شما تایید شد.

━━━━━━━━━━━━━━

✅ سرویس ساخته شد.

🔗 لینک اشتراک

{service['subscription_url']}

از اعتماد شما سپاسگزاریم ❤️

"""

        )

        await query.edit_message_caption(

            caption="✅ پرداخت تایید شد."

        )

    except Exception as e:

        await query.message.reply_text(

            f"❌ خطا\n\n{e}"

        )


# ==========================================================
# Reject Payment
# ==========================================================

async def reject_payment(

    update: Update,

    context: ContextTypes.DEFAULT_TYPE

):

    query = update.callback_query

    await query.answer()

    user_id = int(

        query.data.split("_")[1]

    )

    await context.bot.send_message(

        chat_id=user_id,

        text="""

❌ پرداخت شما توسط ادمین رد شد.

در صورت بروز مشکل با پشتیبانی تماس بگیرید.

"""

    )

    await query.edit_message_caption(

        caption="❌ پرداخت رد شد."

        )
    # ==========================================================
# Zeus Shop VPN PRO
# handlers.py
# Part 6
# ==========================================================


# ==========================================================
# Profile
# ==========================================================

async def profile(

    update: Update,

    context: ContextTypes.DEFAULT_TYPE

):

    query = update.callback_query

    await query.answer()

    user = query.from_user

    text = f"""
👤 پروفایل کاربر

━━━━━━━━━━━━━━

🆔 شناسه

{user.id}

👤 نام

{user.full_name}

📛 یوزرنیم

@{user.username if user.username else "ندارد"}

━━━━━━━━━━━━━━

💎 وضعیت حساب

کاربر ویژه

"""

    keyboard = InlineKeyboardMarkup(

        [

            [

                InlineKeyboardButton(

                    "🌍 سرویس‌های من",

                    callback_data="my_services"

                )

            ],

            [

                InlineKeyboardButton(

                    "⬅ بازگشت",

                    callback_data="main_menu"

                )

            ]

        ]

    )

    await query.edit_message_text(

        text,

        reply_markup=keyboard

    )


# ==========================================================
# My Services
# ==========================================================

async def my_services(

    update: Update,

    context: ContextTypes.DEFAULT_TYPE

):

    query = update.callback_query

    await query.answer()

    try:

        services = panel.get_user_services(

            query.from_user.id

        )

    except:

        services = []

    if not services:

        await query.edit_message_text(

            "❌ هنوز هیچ سرویسی ندارید.",

            reply_markup=InlineKeyboardMarkup(

                [

                    [

                        InlineKeyboardButton(

                            "⬅ بازگشت",

                            callback_data="main_menu"

                        )

                    ]

                ]

            )

        )

        return

    text = "🌍 سرویس‌های شما\n\n"

    for service in services:

        text += f"""

👤 {service['username']}

📊 {service['traffic']}

📅 {service['days']} روز

━━━━━━━━━━━━━━

"""

    keyboard = InlineKeyboardMarkup(

        [

            [

                InlineKeyboardButton(

                    "📊 میزان مصرف",

                    callback_data="usage"

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

                    "⬅ بازگشت",

                    callback_data="profile"

                )

            ]

        ]

    )

    await query.edit_message_text(

        text,

        reply_markup=keyboard

    )


# ==========================================================
# Usage
# ==========================================================

async def usage(

    update: Update,

    context: ContextTypes.DEFAULT_TYPE

):

    query = update.callback_query

    await query.answer()

    await query.edit_message_text(

        """

📊 میزان مصرف

━━━━━━━━━━━━━━

🌐 مصرف امروز

0 GB

📦 حجم باقی‌مانده

در حال دریافت...

""",

        reply_markup=InlineKeyboardMarkup(

            [

                [

                    InlineKeyboardButton(

                        "⬅ بازگشت",

                        callback_data="my_services"

                    )

                ]

            ]

        )

    )


# ==========================================================
# Renew
# ==========================================================

async def renew(

    update: Update,

    context: ContextTypes.DEFAULT_TYPE

):

    query = update.callback_query

    await query.answer()

    await query.edit_message_text(

        """

🔄 تمدید سرویس

برای تمدید سرویس،

پلن جدید خود را انتخاب کنید.

""",

        reply_markup=plans_menu()

    )
    # ==========================================================
# Zeus Shop VPN PRO
# handlers.py
# Part 7
# ==========================================================


# ==========================================================
# Support
# ==========================================================

async def support_menu(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    query = update.callback_query

    await query.answer()

    context.user_data["support"] = True

    await query.edit_message_text(
        """
🎧 پشتیبانی آنلاین

━━━━━━━━━━━━━━

پیام خود را ارسال کنید.

ادمین در اولین فرصت پاسخ خواهد داد.

━━━━━━━━━━━━━━
""",

        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        "⬅ بازگشت",
                        callback_data="main_menu"
                    )
                ]
            ]
        )
    )


# ==========================================================
# Receive Support Message
# ==========================================================

async def support_message(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    if not context.user_data.get("support"):
        return

    context.user_data["support"] = False

    text = update.message.text

    await context.bot.send_message(

        chat_id=ADMIN_ID,

        text=f"""
📩 تیکت جدید

━━━━━━━━━━━━━━

👤 کاربر

{update.effective_user.full_name}

🆔

{update.effective_user.id}

━━━━━━━━━━━━━━

{text}
"""

    )

    await update.message.reply_text(
        "✅ پیام شما ارسال شد."
    )


# ==========================================================
# Wallet
# ==========================================================

async def wallet(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    query = update.callback_query

    await query.answer()

    await query.edit_message_text(

        """
💰 کیف پول

━━━━━━━━━━━━━━

موجودی:

0 تومان

━━━━━━━━━━━━━━

در نسخه بعدی قابلیت شارژ کیف پول اضافه می‌شود.
""",

        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        "⬅ بازگشت",
                        callback_data="main_menu"
                    )
                ]
            ]
        )

    )


# ==========================================================
# Discount
# ==========================================================

async def discount(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    query = update.callback_query

    await query.answer()

    context.user_data["discount"] = True

    await query.edit_message_text(

        """
🎁 کد تخفیف

━━━━━━━━━━━━━━

کد تخفیف خود را ارسال کنید.
""",

        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        "⬅ بازگشت",
                        callback_data="main_menu"
                    )
                ]
            ]
        )

    )


# ==========================================================
# Receive Discount
# ==========================================================

async def receive_discount(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    if not context.user_data.get("discount"):
        return

    context.user_data["discount"] = False

    code = update.message.text.upper()

    if code == "ZEUS20":

        await update.message.reply_text(
            "✅ کد تخفیف ۲۰٪ با موفقیت اعمال شد."
        )

    else:

        await update.message.reply_text(
            "❌ کد تخفیف معتبر نیست."
)
        # ==========================================================
# Zeus Shop VPN PRO
# handlers.py
# Part 8
# Admin Panel
# ==========================================================

from modules.keyboards import admin_menu


# ==========================================================
# Admin Panel
# ==========================================================

async def admin_panel(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    if update.effective_user.id != ADMIN_ID:

        return

    await update.message.reply_text(

        """
👑 پنل مدیریت Zeus Shop

به پنل مدیریت خوش آمدید.
""",

        reply_markup=admin_menu()

    )


# ==========================================================
# Admin Callback
# ==========================================================

async def admin_callback(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    query = update.callback_query

    await query.answer()

    if query.from_user.id != ADMIN_ID:

        return

    data = query.data

    # =======================
    # Users
    # =======================

    if data == "admin_users":

        await query.edit_message_text(

            "👥 تعداد کاربران\n\nدر نسخه بعدی از دیتابیس خوانده می‌شود.",

            reply_markup=admin_menu()

        )

    # =======================
    # Orders
    # =======================

    elif data == "admin_orders":

        await query.edit_message_text(

            "📦 سفارشات\n\nدر نسخه بعدی نمایش داده می‌شود.",

            reply_markup=admin_menu()

        )

    # =======================
    # Payments
    # =======================

    elif data == "admin_payments":

        await query.edit_message_text(

            "💳 پرداخت‌ها\n\nرسیدهای جدید اینجا نمایش داده می‌شوند.",

            reply_markup=admin_menu()

        )

    # =======================
    # Broadcast
    # =======================

    elif data == "admin_broadcast":

        context.user_data["broadcast"] = True

        await query.edit_message_text(

            "📢 پیام همگانی\n\nپیام خود را ارسال کنید."

        )

    # =======================
    # Statistics
    # =======================

    elif data == "admin_stats":

        await query.edit_message_text(

            """
📊 آمار ربات

👥 کاربران:
در حال بارگذاری...

📦 سفارش‌ها:
در حال بارگذاری...

💰 درآمد:
در حال بارگذاری...
""",

            reply_markup=admin_menu()

        )

    # =======================
    # Settings
    # =======================

    elif data == "admin_settings":

        await query.edit_message_text(

            """
⚙ تنظیمات

در نسخه بعدی تکمیل خواهد شد.
""",

            reply_markup=admin_menu()

        )


# ==========================================================
# Broadcast Message
# ==========================================================

async def broadcast_message(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    if update.effective_user.id != ADMIN_ID:

       
