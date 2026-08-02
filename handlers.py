# ==========================================================
# Approve Payment FIX
# ==========================================================


async def approve_payment(

    update: Update,

    context: ContextTypes.DEFAULT_TYPE

):


    query = update.callback_query

    await query.answer()



    # فقط ادمین

    if query.from_user.id != ADMIN_ID:

        return



    user_id = int(
        query.data.split("_")[1]
    )



    order = ORDERS.get(
        user_id
    )


    if not order:

        await query.message.reply_text(
            "❌ سفارش پیدا نشد."
        )

        return



    try:


        vpn_panel = get_panel()



        # ساخت سرویس کامل

        service = vpn_panel.create_subscription(

            telegram_id=user_id,

            days=order["days"],

            traffic_gb=order["traffic_gb"]

        )



        # ذخیره اطلاعات سرویس

        context.user_data["service"] = service



        await context.bot.send_message(

            chat_id=user_id,

            text=f"""

🎉 پرداخت شما تایید شد


━━━━━━━━━━━━━━━━━━


✅ سرویس شما ساخته شد


👤 نام کاربری:

{service["username"]}



📦 حجم:

{order["traffic"]}



📅 مدت:

{order["days"]} روز



⏳ انقضا:

{service["expire"]}



🔗 کانفیگ VLESS:


{service["vless"]}



━━━━━━━━━━━━━━━━━━


🚀 Zeus Shop VPN


"""

        )



        # حذف سفارش

        if user_id in ORDERS:

            del ORDERS[user_id]



        await query.edit_message_caption(

            caption=

            "✅ پرداخت تایید شد\n\n"

            "🚀 سرویس ساخته و برای کاربر ارسال شد."

        )



    except Exception as e:


        await query.message.reply_text(

            f"""

❌ خطا در ساخت سرویس


{e}

"""

        )
        # -------------------------------------------------------
# Get User Services
# -------------------------------------------------------

def get_user_services(
    self,
    telegram_id
):

    clients = self.get_clients()


    services = []


    for client in clients:


        if str(client.get("tgId")) == str(telegram_id):


            services.append({

                "email": client.get(
                    "email",
                    "Unknown"
                ),

                "uuid": client.get(
                    "id",
                    ""
                ),

                "traffic": round(

                    int(
                        client.get(
                            "totalGB",
                            0
                        )
                    )
                    /
                    (1024 ** 3),

                    2

                ),

                "expire": self.format_expire(

                    client.get(
                        "expiryTime",
                        0
                    )

                ),

                "enable": client.get(
                    "enable",
                    False
                )

            })


    return services
    # ==========================================================
# Text Message Router FIX
# ==========================================================


async def text_router(

    update: Update,

    context: ContextTypes.DEFAULT_TYPE

):


    # حجم دلخواه

    if context.user_data.get(
        "waiting_custom_gb"
    ):

        await custom_volume(
            update,
            context
        )

        return



    # پشتیبانی

    if context.user_data.get(
        "support"
    ):

        await support_message(
            update,
            context
        )

        return



    # کد تخفیف

    if context.user_data.get(
        "discount"
    ):

        await receive_discount(
            update,
            context
        )

        return



    # پیام همگانی ادمین

    if context.user_data.get(
        "broadcast"
    ):

        await broadcast_message(
            update,
            context
        )

        return



    # هیچ حالت فعالی نیست

    await update.message.reply_text(

        "❌ دستور یا گزینه‌ای انتخاب نشده است."

    )
    # ==========================================================
# Register All Handlers FINAL
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
    # Main Menu
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
            pattern="^payment$"
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
    # User Features
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
    # Receipt Photo
    # ==========================


    application.add_handler(

        MessageHandler(

            filters.PHOTO,

            receipt_handler

        )

    )



    # ==========================
    # Text Router
    # ==========================


    application.add_handler(

        MessageHandler(

            filters.TEXT & ~filters.COMMAND,

            text_router

        )

    )



    print(
        "✅ Zeus Shop VPN PRO handlers loaded"
    )
