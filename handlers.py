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
# Zeus Shop VPN PRO FINAL
# handlers.py
# Part 6/8
# ==========================================================


# ==========================
# Profile Handler
# ==========================

async def profile(update: Update, context: ContextTypes.DEFAULT_TYPE):

    user = update.effective_user

    text = f"""
👤 پروفایل کاربر

━━━━━━━━━━━━━━━━━━

🆔 آیدی تلگرام:
`{user.id}`

👤 نام:
{user.first_name}

━━━━━━━━━━━━━━━━━━

📡 وضعیت اشتراک:
❌ هنوز اشتراکی فعال نیست

برای خرید اشتراک از منوی اصلی استفاده کنید.

"""

    keyboard = [
        [
            InlineKeyboardButton(
                "🛒 خرید اشتراک",
                callback_data="buy"
            )
        ],
        [
            InlineKeyboardButton(
                "🔙 بازگشت",
                callback_data="back_menu"
            )
        ]
    ]

    await update.callback_query.edit_message_text(
        text=text,
        reply_markup=InlineKeyboardMarkup(keyboard),
        parse_mode="Markdown"
    )



# ==========================
# Support Handler
# ==========================

async def support(update: Update, context: ContextTypes.DEFAULT_TYPE):

    text = """
🆘 پشتیبانی Zeus Shop VPN

━━━━━━━━━━━━━━━━━━

اگر مشکلی در اتصال یا خرید دارید
با پشتیبانی تماس بگیرید.

📞 پشتیبانی:
@YourSupport

━━━━━━━━━━━━━━━━━━

"""

    keyboard = [
        [
            InlineKeyboardButton(
                "💬 تماس با پشتیبانی",
                url="https://t.me/YourSupport"
            )
        ],
        [
            InlineKeyboardButton(
                "🔙 بازگشت",
                callback_data="back_menu"
            )
        ]
    ]

    await update.callback_query.edit_message_text(
        text=text,
        reply_markup=InlineKeyboardMarkup(keyboard)
    )



# ==========================
# Download Handler
# ==========================

async def download(update: Update, context: ContextTypes.DEFAULT_TYPE):

    text = """
📲 دانلود برنامه اتصال

━━━━━━━━━━━━━━━━━━

🤖 Android:
v2rayNG

🍎 iPhone:
Streisand

💻 Windows:
v2rayN

بعد از دریافت کانفیگ،
داخل برنامه وارد کنید.

━━━━━━━━━━━━━━━━━━
"""

    keyboard = [
        [
            InlineKeyboardButton(
                "🔙 بازگشت",
                callback_data="back_menu"
            )
        ]
    ]

    await update.callback_query.edit_message_text(
        text=text,
        reply_markup=InlineKeyboardMarkup(keyboard)
  )
  # ==========================================================
# Zeus Shop VPN PRO FINAL
# handlers.py
# Part 7/8
# ==========================================================


# ==========================
# Buy Subscription Handler
# ==========================

async def buy(update: Update, context: ContextTypes.DEFAULT_TYPE):

    text = """
🛒 خرید اشتراک Zeus Shop VPN

━━━━━━━━━━━━━━━━━━

پلن مورد نظر خود را انتخاب کنید:

⚡ 1 ماهه
🔥 3 ماهه
👑 6 ماهه
💎 1 ساله

━━━━━━━━━━━━━━━━━━
"""

    keyboard = [
        [
            InlineKeyboardButton(
                "⚡ 1 ماهه",
                callback_data="plan_1"
            )
        ],
        [
            InlineKeyboardButton(
                "🔥 3 ماهه",
                callback_data="plan_3"
            )
        ],
        [
            InlineKeyboardButton(
                "👑 6 ماهه",
                callback_data="plan_6"
            )
        ],
        [
            InlineKeyboardButton(
                "💎 1 ساله",
                callback_data="plan_12"
            )
        ],
        [
            InlineKeyboardButton(
                "🔙 بازگشت",
                callback_data="back_menu"
            )
        ]
    ]

    await update.callback_query.edit_message_text(
        text=text,
        reply_markup=InlineKeyboardMarkup(keyboard)
    )



# ==========================
# Plan Select Handler
# ==========================

async def select_plan(update: Update, context: ContextTypes.DEFAULT_TYPE):

    query = update.callback_query

    plan = query.data.replace(
        "plan_",
        ""
    )

    prices = {
        "1": "50,000 تومان",
        "3": "130,000 تومان",
        "6": "240,000 تومان",
        "12": "450,000 تومان"
    }

    names = {
        "1": "یک ماهه",
        "3": "سه ماهه",
        "6": "شش ماهه",
        "12": "یک ساله"
    }


    text = f"""
💳 پرداخت اشتراک

━━━━━━━━━━━━━━━━━━

📦 پلن:
{names[plan]}

💰 قیمت:
{prices[plan]}

━━━━━━━━━━━━━━━━━━

بعد از پرداخت، رسید را ارسال کنید.

"""

    keyboard = [
        [
            InlineKeyboardButton(
                "💳 اطلاعات پرداخت",
                callback_data="payment"
            )
        ],
        [
            InlineKeyboardButton(
                "🔙 برگشت",
                callback_data="buy"
            )
        ]
    ]


    await query.edit_message_text(
        text=text,
        reply_markup=InlineKeyboardMarkup(keyboard)
    )



# ==========================
# Payment Info
# ==========================

async def payment(update: Update, context: ContextTypes.DEFAULT_TYPE):

    text = """
💳 اطلاعات پرداخت

━━━━━━━━━━━━━━━━━━

🏦 شماره کارت:

0000-0000-0000-0000

👤 به نام:
نام صاحب کارت

━━━━━━━━━━━━━━━━━━

بعد از واریز، عکس رسید را ارسال کنید.

"""

    keyboard = [
        [
            InlineKeyboardButton(
                "📤 ارسال رسید",
                callback_data="send_receipt"
            )
        ],
        [
            InlineKeyboardButton(
                "🔙 بازگشت",
                callback_data="buy"
            )
        ]
    ]


    await update.callback_query.edit_message_text(
        text=text,
        reply_markup=InlineKeyboardMarkup(keyboard)
    )
  # ==========================================================
# Zeus Shop VPN PRO FINAL
# handlers.py
# Part 8/8 FINAL
# ==========================================================


# ==========================
# Callback Router
# ==========================

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):

    query = update.callback_query

    await query.answer()

    data = query.data


    if data == "profile":
        await profile(update, context)


    elif data == "support":
        await support(update, context)


    elif data == "download":
        await download(update, context)


    elif data == "buy":
        await buy(update, context)


    elif data.startswith("plan_"):
        await select_plan(update, context)


    elif data == "payment":
        await payment(update, context)


    elif data == "back_menu":

        await query.edit_message_text(
            text=WELCOME_TEXT,
            reply_markup=main_menu()
        )



# ==========================
# Register Handlers
# ==========================

def register_handlers(application):


    application.add_handler(
        CommandHandler(
            "start",
            start
        )
    )


    application.add_handler(
        CallbackQueryHandler(
            button_handler
        )
    )


    application.add_handler(
        MessageHandler(
            filters.PHOTO,
            receipt_handler
        )
    )


# ==========================================================
# END OF handlers.py
# ==========================================================
