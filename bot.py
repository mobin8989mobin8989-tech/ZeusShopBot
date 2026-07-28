# ==========================================================
# ZeusShopBot
# bot.py
# ==========================================================

from telegram.ext import Application

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
    # Register
    # ======================================================

    def register_handlers(self):

        register_handlers(
            self.app
        )


    # ======================================================
    # Run Bot
    # ======================================================

    def run(self):

        self.register_handlers()

        print(
            "🚀 Zeus Shop Bot Started..."
        )

        self.app.run_polling()



# ==========================================================
# Start
# ==========================================================

if __name__ == "__main__":

    bot = ZeusBot()

    bot.run()
