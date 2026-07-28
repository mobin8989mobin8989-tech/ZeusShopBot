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
    ContextTypes
)


from modules.keyboards import (
    main_menu,
    plans_menu,
    admin_menu
)


from modules.users import users


from modules.panel import Panel


from config import (
    ADMIN_ID,
    CHANNEL,
    PLANS
)



# اتصال به پنل 3X-UI

panel = Panel()



# ==========================================================
# Welcome Text
# ==========================================================


WELCOME_TEXT = f"""

╔══════════════════════╗
      👑 Zeus Shop VPN
╚══════════════════════╝


🚀 به فروشگاه حرفه‌ای Zeus Shop خوش آمدید.


━━━━━━━━━━━━━━━━━━


⚡ تحویل خودکار سرویس

🛡 امنیت و پایداری بالا

🌍 سرورهای پرسرعت

📡 مناسب تمام اپراتورها

🎁 تخفیف ویژه کاربران


━━━━━━━━━━━━━━━━━━


📢 کانال اطلاع‌رسانی:

{CHANNEL}


👇 از منوی زیر انتخاب کنید.


"""



# ==========================================================
# Start Command
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

        WELCOME_TEXT,

        reply_markup=main_menu()

    )
    # ==========================================================
# Payment System
# Part 3
# ==========================================================


from config import (
    CARD_NUMBER,
    CARD_HOLDER,
    BANK_NAME
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



    # ==========================
    # Custom Volume
    # ==========================


    if "custom_price" in context.user_data:


        price = context.user_data["custom_price"]


        traffic = (

            f"{context.user_data['custom_gb']} GB"

        )


        traffic_gb = context.user_data["custom_gb"]


        days = 30



    # ==========================
    # Normal Plan
    # ==========================


    else:


        plan = PLANS[

            context.user_data["selected_plan"]

        ]


        price = plan["price"]


        traffic = plan["traffic"]


        traffic_gb = int(

            traffic.replace(

                "GB",

                ""

            )

        )


        days = plan["days"]





    # ذخیره سفارش

    context.user_data["order"] = {


        "price": price,


        "traffic": traffic,


        "traffic_gb": traffic_gb,


        "days": days


    }



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

💳 اطلاعات پرداخت Zeus Shop


━━━━━━━━━━━━━━━━━━


💰 مبلغ:

{price:,} تومان



🌐 حجم:

{traffic}



📅 مدت:

{days} روز



━━━━━━━━━━━━━━━━━━


🏦 بانک:

{BANK_NAME}


💳 شماره کارت:

`{CARD_NUMBER}`



👤 صاحب حساب:

{CARD_HOLDER}



━━━━━━━━━━━━━━━━━━


بعد از پرداخت، رسید را ارسال کنید.

"""



    await query.edit_message_text(

        text,

        parse_mode="Markdown",

        reply_markup=keyboard

    )






# ==========================================================
# Send Receipt Request
# ==========================================================


async def send_receipt(

    update: Update,

    context: ContextTypes.DEFAULT_TYPE

):


    query = update.callback_query


    await query.answer()



    await query.message.reply_text(

        """

📷 لطفاً تصویر رسید پرداخت را ارسال کنید.


بعد از بررسی، سرویس شما خودکار ساخته می‌شود.

"""

    )






# ==========================================================
# Receive Receipt
# ==========================================================


async def receipt_handler(

    update: Update,

    context: ContextTypes.DEFAULT_TYPE

):


    if not context.user_data.get(

        "waiting_receipt"

    ):

        return




    if not update.message.photo:


        await update.message.reply_text(

            "❌ لطفاً فقط تصویر رسید ارسال کنید."

        )


        return





    photo_id = update.message.photo[-1].file_id



    context.user_data["receipt"] = photo_id



    context.user_data["waiting_receipt"] = False





    await update.message.reply_text(

        """

✅ رسید دریافت شد.


⏳ منتظر تایید مدیریت باشید.


پس از تایید، لینک اتصال برای شما ارسال می‌شود.

"""

    )




    # ارسال به ادمین


    order = context.user_data.get(

        "order",

        {}

    )



    keyboard = InlineKeyboardMarkup(

        [

            [

                InlineKeyboardButton(

                    "✅ تایید و ساخت سرویس",

                    callback_data=f"approve_{update.effective_user.id}"

                )

            ],


            [

                InlineKeyboardButton(

                    "❌ رد پرداخت",

                    callback_data=f"reject_{update.effective_user.id}"

                )

            ]

        ]

    )



    await context.bot.send_photo(

        chat_id=ADMIN_ID,

        photo=photo_id,

        caption=f"""

💳 پرداخت جدید Zeus Shop


━━━━━━━━━━━━━━


👤 کاربر:

{update.effective_user.full_name}



🆔 آیدی:

{update.effective_user.id}



🌐 حجم:

{order.get('traffic','نامشخص')}



📅 مدت:

{order.get('days','نامشخص')} روز



💰 مبلغ:

{order.get('price',0):,} تومان



━━━━━━━━━━━━━━

آماده بررسی

""",

        reply_markup=keyboard

    )
    # ==========================================================
# Admin Payment Approve System
# Part 4
# ==========================================================



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



        # گرفتن سفارش ذخیره شده

        order = context.user_data.get(

            "order"

        )



        if not order:


            raise Exception(

                "اطلاعات سفارش پیدا نشد"

            )





        # =================================
        # ساخت کاربر در 3X-UI
        # =================================


        service = panel.create_service(


            telegram_id=user_id,


            days=order["days"],


            traffic_gb=order["traffic_gb"]


        )





        # =================================
        # ارسال سرویس به مشتری
        # =================================


        await context.bot.send_message(


            chat_id=user_id,


            text=f"""

🎉 پرداخت شما تایید شد


━━━━━━━━━━━━━━━━


✅ سرویس شما ساخته شد


👤 نام کاربری:

{service['username']}



🔗 لینک اتصال:


{service['subscription_url']}



━━━━━━━━━━━━━━━━


🚀 Zeus Shop VPN


ممنون از اعتماد شما ❤️

"""

        )





        # تغییر پیام ادمین


        await query.edit_message_caption(


            caption=

            "✅ پرداخت تایید شد\n\n"

            "🚀 سرویس 3X-UI ساخته شد."

        )




    except Exception as e:



        await query.message.reply_text(


            f"""

❌ خطا در ساخت سرویس


{e}

"""

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

❌ پرداخت شما رد شد.


در صورت اشتباه با پشتیبانی تماس بگیرید.

"""

    )




    await query.edit_message_caption(


        caption="❌ پرداخت رد شد."

    )
    # ==========================================================
# User Profile System
# Part 5
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


🆔 شناسه:

{user.id}



👤 نام:

{user.full_name}



📛 یوزرنیم:

@{user.username if user.username else "ندارد"}



━━━━━━━━━━━━━━


⭐ وضعیت:

کاربر Zeus Shop


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


    except Exception:


        services = []





    if not services:



        await query.edit_message_text(


            """

❌ شما هنوز سرویسی ندارید.


برای خرید سرویس از منوی خرید استفاده کنید.


""",


            reply_markup=InlineKeyboardMarkup(

                [

                    [

                        InlineKeyboardButton(

                            "🛒 خرید سرویس",

                            callback_data="buy_service"

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

        )


        return






    text = """

🌍 سرویس‌های شما


━━━━━━━━━━━━━━


"""



    for service in services:



        text += f"""

👤 نام:

{service.get('email')}



📊 حجم:

{service.get('totalGB','نامشخص')}



━━━━━━━━━━━━━━


"""





    keyboard = InlineKeyboardMarkup(

        [

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
# Renew Service
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


پلن موردنظر برای تمدید را انتخاب کنید.


""",


        reply_markup=plans_menu()

    )
    # ==========================================================
# Support / Wallet / Discount
# Part 6
# ==========================================================



# ==========================================================
# Support Menu
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

🎧 پشتیبانی آنلاین Zeus Shop


━━━━━━━━━━━━━━


پیام خود را ارسال کنید.


پشتیبانی در اولین فرصت پاسخ می‌دهد.


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


    if not context.user_data.get(

        "support"

    ):

        return




    context.user_data["support"] = False



    text = update.message.text



    await context.bot.send_message(


        chat_id=ADMIN_ID,


        text=f"""

📩 تیکت جدید Zeus Shop


━━━━━━━━━━━━━━


👤 کاربر:

{update.effective_user.full_name}



🆔 آیدی:

{update.effective_user.id}



━━━━━━━━━━━━━━


{text}

"""

    )



    await update.message.reply_text(


        "✅ پیام شما برای پشتیبانی ارسال شد."

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


موجودی فعلی:


0 تومان



━━━━━━━━━━━━━━


در نسخه بعدی امکان شارژ کیف پول اضافه می‌شود.


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
# Check Discount
# ==========================================================


async def receive_discount(

    update: Update,

    context: ContextTypes.DEFAULT_TYPE

):


    if not context.user_data.get(

        "discount"

    ):

        return




    context.user_data["discount"] = False



    code = update.message.text.upper()



    if code == "ZEUS20":



        await update.message.reply_text(


            """

✅ کد تخفیف فعال شد.


🎁 ۲۰٪ تخفیف برای خرید شما اعمال شد.


"""

        )



    else:



        await update.message.reply_text(


            "❌ کد تخفیف اشتباه است."

    )
        # ==========================================================
# Zeus Shop VPN PRO
# handlers.py
# Part 8
# Register Handlers
# ==========================================================


from telegram.ext import (
    CommandHandler,
    CallbackQueryHandler,
    MessageHandler,
    filters
)



# ==========================================================
# Register All Handlers
# ==========================================================


def register_handlers(application):


    # ==========================
    # Commands
    # ==========================


    application.add_handler(

        CommandHandler(

            "start",

            start

        )

    )


    application.add_handler(

        CommandHandler(

            "admin",

            admin_panel

        )

    )




    # ==========================
    # Buttons
    # ==========================


    application.add_handler(

        CallbackQueryHandler(

            buy_service,

            pattern="^buy_service$"

        )

    )



    application.add_handler(

        CallbackQueryHandler(

            select_plan,

            pattern="^plan_"

        )

    )



    application.add_handler(

        CallbackQueryHandler(

            payment,

            pattern="^payment"

        )

    )



    application.add_handler(

        CallbackQueryHandler(

            send_receipt,

            pattern="^send_receipt$"

        )

    )



    application.add_handler(

        CallbackQueryHandler(

            approve_payment,

            pattern="^approve_"

        )

    )



    application.add_handler(

        CallbackQueryHandler(

            reject_payment,

            pattern="^reject_"

        )

    )



    application.add_handler(

        CallbackQueryHandler(

            profile,

            pattern="^profile$"

        )

    )



    application.add_handler(

        CallbackQueryHandler(

            my_services,

            pattern="^my_services$"

        )

    )



    application.add_handler(

        CallbackQueryHandler(

            renew,

            pattern="^renew$"

        )

    )



    application.add_handler(

        CallbackQueryHandler(

            support_menu,

            pattern="^support$"

        )

    )



    application.add_handler(

        CallbackQueryHandler(

            wallet,

            pattern="^wallet$"

        )

    )



    application.add_handler(

        CallbackQueryHandler(

            discount,

            pattern="^discount$"

        )

    )



    application.add_handler(

        CallbackQueryHandler(

            admin_callback

        )

    )





    # ==========================
    # Messages
    # ==========================



    application.add_handler(

        MessageHandler(

            filters.TEXT

            &

            ~filters.COMMAND,

            custom_volume

        )

    )



    application.add_handler(

        MessageHandler(

            filters.TEXT

            &

            ~filters.COMMAND,

            support_message

        )

    )



    application.add_handler(

        MessageHandler(

            filters.TEXT

            &

            ~filters.COMMAND,

            receive_discount

        )

    )



    application.add_handler(

        MessageHandler(

            filters.PHOTO,

            receipt_handler

        )

    )
