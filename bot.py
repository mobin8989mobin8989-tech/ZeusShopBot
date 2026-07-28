# ==========================================================
# ZeusShopBot
# bot.py
# ==========================================================


from telegram import Update

from telegram.ext import (
    Application,
    CommandHandler,
    ContextTypes,
)

from config import BOT_TOKEN

from handlers import register_handlers



class ZeusBot:


    def __init__(self):

        self.app = (
            Application
            .builder()
            .token(BOT_TOKEN)
            .build()
        )


    # ======================================================
    # Start
    # ======================================================

    async def start(
        self,
        update: Update,
        context: ContextTypes.DEFAULT_TYPE
    ):

        await update.message.reply_text(
            "👑 به Zeus Shop VPN خوش آمدید."
        )



    # ======================================================
    # Register
    # ======================================================

    def register_handlers(self):


        # اتصال تمام بخش‌های handlers.py

        register_handlers(
            self.app
        )


        # دستور start

        self.app.add_handler(
            CommandHandler(
                "start",
                self.start
            )
        )



    # ======================================================
    # Run
    # ======================================================

    def run(self):


        self.register_handlers()


        print(
            "🚀 Zeus Shop Bot Started..."
        )


        self.app.run_polling()





# ==========================================================
# Run Bot
# ==========================================================


if __name__ == "__main__":


    bot = ZeusBot()

    bot.run()
