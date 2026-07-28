# ==========================================================
# ZeusShopBot
# bot.py
# ==========================================================

from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    CallbackQueryHandler,
    MessageHandler,
    ContextTypes,
    filters,
)

from config import BOT_TOKEN


class ZeusBot:

    def __init__(self):

        self.app = Application.builder().token(BOT_TOKEN).build()

    # ======================================================

    async def start(
        self,
        update: Update,
        context: ContextTypes.DEFAULT_TYPE,
    ):

        await update.message.reply_text(
            "👋 به Zeus Shop خوش آمدید."
        )

    # ======================================================

    async def help(
        self,
        update: Update,
        context: ContextTypes.DEFAULT_TYPE,
    ):

        await update.message.reply_text(
            "پنل مدیریت در حال آماده سازی است."
        )

    # ======================================================

    def register_handlers(self):

        self.app.add_handler(
            CommandHandler("start", self.start)
        )

        self.app.add_handler(
            CommandHandler("help", self.help)
        )

    # ======================================================

    def run(self):

        self.register_handlers()

        print("Zeus Shop Started...")

        self.app.run_polling()


bot = ZeusBot()
