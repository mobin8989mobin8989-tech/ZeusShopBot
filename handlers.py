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


from config import (
    ADMIN_ID,
    CHANNEL,
    PLANS,
    PRICE_PER_GB,
    CARD_NUMBER,
    CARD_HOLDER,
    BANK_NAME
)


from modules.keyboards import (
    main_menu,
    plans_menu,
    admin_menu
)


from modules.users import users


from modules.panel import Panel



# ==========================================================
# 3X-UI Connection
# ==========================================================


panel = Panel()



# ==========================================================
# Welcome Text
# ==========================================================


WELCOME_TEXT = f"""

╔══════════════════════╗
       👑 Zeus Shop VPN
╚══════════════════════╝


🚀 فروشگاه حرفه‌ای VPN


━━━━━━━━━━━━━━━━━━


⚡ تحویل خودکار سرویس

🌍 سرورهای پرسرعت

🛡 اتصال پایدار

📡 مناسب تمام اپراتورها

🎁 تخفیف ویژه کاربران


━━━━━━━━━━━━━━━━━━


📢 کانال اطلاع‌رسانی:

{CHANNEL}


👇 گزینه موردنظر را انتخاب کنید.


"""



# ==========================================================
# Start
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
# Zeus Shop VPN PRO
# handlers.py
# Part 2
# Buy System
# ==========================================================



# ==========================================================
# Buy Service Menu
# ==========================================================


BUY_TEXT = """

🛒 خرید اشتراک Zeus Shop VPN


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


پلن موردنظر را انتخاب کنید.


"""





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






    # ==============================
    # Custom Volume
    # ==============================


    if plan_key == "custom":


        context.user_data["waiting_custom_gb"] = True



        await query.edit_message_text(

            f"""

🛠 حجم دلخواه


━━━━━━━━━━━━━━━━━━


حجم موردنظر خود را وارد کنید.


💰 قیمت هر گیگ:

{PRICE_PER_GB:,} تومان


مثال:

50


"""

        )


        return








    # ==============================
    # Save Order
    # ==============================



    context.user_data["order"] = {


        "name": plan["name"],

        "traffic": plan["traffic"],

        "traffic_gb": plan.get("gb",0),

        "days": plan["days"],

        "price": plan["price"]

    }





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


        f"""

✅ پلن انتخاب شد


━━━━━━━━━━━━━━━━━━


📦 نام:

{plan["name"]}



🌐 حجم:

{plan["traffic"]}



📅 مدت:

{plan["days"]} روز



💰 مبلغ:

{plan["price"]:,} تومان



━━━━━━━━━━━━━━━━━━


برای پرداخت کلیک کنید.


""",


        reply_markup=keyboard

    )








# ==========================================================
# Custom Volume Handler
# ==========================================================


async def custom_volume(

    update: Update,

    context: ContextTypes.DEFAULT_TYPE

):


    if not context.user_data.get(

        "waiting_custom_gb"

    ):


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







    price = gb * PRICE_PER_GB





    context.user_data["waiting_custom_gb"] = False



    context.user_data["order"] = {


        "name": "🛠 حجم دلخواه",


        "traffic": f"{gb}GB",


        "traffic_gb": gb,


        "days": 30,


        "price": price


    }






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






    await update.message.reply_text(



        f"""

✅ حجم ثبت شد


━━━━━━━━━━━━━━━━━━


🌐 حجم:

{gb} GB



📅 مدت:

30 روز



💰 مبلغ:

{price:,} تومان



━━━━━━━━━━━━━━━━━━


برای پرداخت اقدام کنید.


""",


        reply_markup=keyboard

    )
    # ==========================================================
# Zeus Shop VPN PRO
# handlers.py
# Part 3
# Payment System
# ==========================================================



# ==========================================================
# Payment Page
# ==========================================================


async def payment(

    update: Update,

    context: ContextTypes.DEFAULT_TYPE

):


    query = update.callback_query


    await query.answer()



    order = context.user_data.get("order")



    if not order:



        await query.edit_message_text(

            "❌ سفارش پیدا نشد. دوباره اقدام کنید."

        )

        return





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

💳 پرداخت Zeus Shop VPN


━━━━━━━━━━━━━━━━━━


📦 سرویس:

{order["name"]}



🌐 حجم:

{order["traffic"]}



📅 مدت:

{order["days"]} روز



💰 مبلغ:

{order["price"]:,} تومان



━━━━━━━━━━━━━━━━━━


🏦 بانک:

{BANK_NAME}



💳 شماره کارت:

`{CARD_NUMBER}`



👤 صاحب حساب:

{CARD_HOLDER}



━━━━━━━━━━━━━━━━━━


بعد از پرداخت، تصویر رسید را ارسال کنید.


"""






    await query.edit_message_text(

        text,

        parse_mode="Markdown",

        reply_markup=keyboard

    )








# ==========================================================
# Send Receipt Button
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


پس از تایید مدیریت، سرویس شما ساخته می‌شود.


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







    await update.message.reply_text(

        """

✅ رسید شما دریافت شد.


⏳ منتظر تایید مدیریت باشید.


"""

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



📦 سرویس:

{order.get("name")}



🌐 حجم:

{order.get("traffic")}



📅 مدت:

{order.get("days")} روز



💰 مبلغ:

{order.get("price"):,} تومان



━━━━━━━━━━━━━━


منتظر بررسی ادمین

""",


        reply_markup=keyboard

    )
    # ==========================================================
# Zeus Shop VPN PRO
# handlers.py
# Part 4
# Admin Payment System
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



        order = context.user_data.get(

            "order"

        )



        if not order:


            raise Exception(

                "اطلاعات سفارش پیدا نشد"

            )







        # ==================================
        # ساخت سرویس در 3X-UI
        # ==================================


        service = panel.create_service(


            telegram_id=user_id,


            traffic_gb=order["traffic_gb"],


            days=order["days"]


        )







        # ==================================
        # ارسال اطلاعات به مشتری
        # ==================================


        await context.bot.send_message(


            chat_id=user_id,


            text=f"""

🎉 پرداخت شما تایید شد


━━━━━━━━━━━━━━━━━━


✅ سرویس شما ساخته شد



👤 نام کاربری:

{service.get("username","")}



🔗 لینک اتصال:

{service.get("subscription_url","")}



━━━━━━━━━━━━━━━━━━


🚀 Zeus Shop VPN


ممنون از اعتماد شما ❤️


"""

        )







        await query.edit_message_caption(


            caption=

            "✅ پرداخت تایید شد\n\n"

            "🚀 سرویس با موفقیت ساخته شد."

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

❌ پرداخت شما تایید نشد.


اگر فکر می‌کنید اشتباهی رخ داده است،

با پشتیبانی تماس بگیرید.


"""

    )







    await query.edit_message_caption(


        caption=

        "❌ پرداخت رد شد."

        )
    # ==========================================================
# Zeus Shop VPN PRO
# handlers.py
# Part 5
# User Profile + Services
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

👤 پروفایل کاربر Zeus Shop


━━━━━━━━━━━━━━━━━━


🆔 آیدی:

{user.id}



👤 نام:

{user.full_name}



📛 یوزرنیم:

@{user.username if user.username else "ندارد"}



━━━━━━━━━━━━━━━━━━


⭐ وضعیت:

کاربر فعال Zeus Shop


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

❌ شما هنوز هیچ سرویسی ندارید.


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

                            callback_data="profile"

                        )

                    ]

                ]

            )

        )


        return










    text = """

🌍 سرویس‌های من


━━━━━━━━━━━━━━━━━━


"""







    for service in services:



        text += f"""

👤 نام:

{service.get("username","نامشخص")}



📊 حجم:

{service.get("traffic","نامشخص")}



📅 انقضا:

{service.get("expire","نامشخص")}



🔗 لینک:

{service.get("subscription_url","ندارد")}



━━━━━━━━━━━━━━━━━━


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


پلن موردنظر خود را انتخاب کنید.


""",


        reply_markup=plans_menu()

    )
    # ==========================================================
# Zeus Shop VPN PRO
# handlers.py
# Part 6
# Support + Wallet + Discount
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


━━━━━━━━━━━━━━━━━━


پیام خود را ارسال کنید.


پشتیبانی در اولین فرصت پاسخ خواهد داد.


━━━━━━━━━━━━━━━━━━


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



    message = update.message.text





    await context.bot.send_message(


        chat_id=ADMIN_ID,


        text=f"""

📩 تیکت جدید Zeus Shop


━━━━━━━━━━━━━━━━━━


👤 کاربر:

{update.effective_user.full_name}



🆔 آیدی:

{update.effective_user.id}



━━━━━━━━━━━━━━━━━━


💬 پیام:


{message}


"""

    )







    await update.message.reply_text(


        """

✅ پیام شما ارسال شد.


پشتیبانی به زودی پاسخ می‌دهد.


"""

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

💰 کیف پول Zeus Shop


━━━━━━━━━━━━━━━━━━


💳 موجودی:


0 تومان



━━━━━━━━━━━━━━━━━━


این بخش در نسخه بعدی فعال می‌شود.


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


━━━━━━━━━━━━━━━━━━


کد تخفیف خود را ارسال کنید.


مثال:

ZEUS20


━━━━━━━━━━━━━━━━━━


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
# Check Discount Code
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


            """

❌ کد تخفیف اشتباه است.


"""

        )
        # ==========================================================
# Zeus Shop VPN PRO
# handlers.py
# Part 7
# Admin Panel
# ==========================================================






# ==========================================================
# Admin Panel Command
# ==========================================================


async def admin_panel(

    update: Update,

    context: ContextTypes.DEFAULT_TYPE

):


    user = update.effective_user



    if user.id != ADMIN_ID:


        await update.message.reply_text(

            "❌ شما دسترسی ادمین ندارید."

        )

        return






    await update.message.reply_text(


        """

👑 پنل مدیریت Zeus Shop


━━━━━━━━━━━━━━━━━━


به بخش مدیریت خوش آمدید.


"""

,

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






    # ==========================
    # Users
    # ==========================


    if data == "admin_users":



        await query.edit_message_text(


            """

👥 کاربران


━━━━━━━━━━━━━━━━━━


لیست کاربران در حال دریافت است.


"""

,

            reply_markup=admin_menu()

        )








    # ==========================
    # Orders
    # ==========================


    elif data == "admin_orders":



        await query.edit_message_text(


            """

📦 سفارشات


━━━━━━━━━━━━━━━━━━


سفارش‌ها در این بخش نمایش داده می‌شوند.


"""

,

            reply_markup=admin_menu()

        )








    # ==========================
    # Payments
    # ==========================


    elif data == "admin_payments":



        await query.edit_message_text(


            """

💳 پرداخت‌ها


━━━━━━━━━━━━━━━━━━


رسیدهای پرداخت کاربران اینجا مدیریت می‌شود.


"""

,

            reply_markup=admin_menu()

        )








    # ==========================
    # Statistics
    # ==========================


    elif data == "admin_stats":



        await query.edit_message_text(


            """

📊 آمار Zeus Shop


━━━━━━━━━━━━━━━━━━


👥 کاربران:

در حال دریافت...


📦 سرویس‌ها:

در حال دریافت...


💰 درآمد:

در حال دریافت...



"""

,

            reply_markup=admin_menu()

        )








    # ==========================
    # Broadcast
    # ==========================


    elif data == "admin_broadcast":



        context.user_data["broadcast"] = True




        await query.edit_message_text(


            """

📢 ارسال پیام همگانی


━━━━━━━━━━━━━━━━━━


متن پیام را ارسال کنید.


"""

        )








    # ==========================
    # Settings
    # ==========================


    elif data == "admin_settings":



        await query.edit_message_text(


            """

⚙ تنظیمات


━━━━━━━━━━━━━━━━━━


تنظیمات ربات در حال توسعه است.


"""

,

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


        return




    if not context.user_data.get(

        "broadcast"

    ):


        return






    context.user_data["broadcast"] = False






    message = update.message.text






    await update.message.reply_text(


        """

✅ پیام همگانی ثبت شد.


ارسال برای کاربران شروع می‌شود.


"""

    )






    # در نسخه دیتابیس واقعی
    # لیست کاربران از database گرفته می‌شود
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
    # Main Buttons
    # ==========================


    application.add_handler(

        CallbackQueryHandler(

            buy_service,

            pattern="^buy_service$"

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






    # ==========================
    # Plans
    # ==========================


    application.add_handler(

        CallbackQueryHandler(

            select_plan,

            pattern="^plan_"

        )

    )







    # ==========================
    # Payment
    # ==========================


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







    # ==========================
    # Support
    # ==========================


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






    # ==========================
    # Admin
    # ==========================


    application.add_handler(

        CallbackQueryHandler(

            admin_callback,

            pattern="^admin_"

        )

    )







    # ==========================
    # Messages
    # ==========================


    application.add_handler(

        MessageHandler(

            filters.PHOTO,

            receipt_handler

        )

    )




    application.add_handler(

        MessageHandler(

            filters.TEXT & ~filters.COMMAND,

            custom_volume

        )

    )




    application.add_handler(

        MessageHandler(

            filters.TEXT & ~filters.COMMAND,

            support_message

        )

    )




    application.add_handler(

        MessageHandler(

            filters.TEXT & ~filters.COMMAND,

            receive_discount

        )

    )




    application.add_handler(

        MessageHandler(

            filters.TEXT & ~filters.COMMAND,

            broadcast_message

        )

    )
