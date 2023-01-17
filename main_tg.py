import os
from functools import partial
from dotenv import load_dotenv

from telegram import Update, ForceReply
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext


def start(update: Update, context: CallbackContext) -> None:
    """Send a message when the command /start is issued."""
    user = update.effective_user
    update.message.reply_markdown_v2(
        fr'Hi {user.mention_markdown_v2()}\!',
        reply_markup=ForceReply(selective=True),
    )


def reply(update: Update, context: CallbackContext) -> None:
    update.message.reply_text(update.message.text)


def main() -> None:
    """Start the bot."""

    load_dotenv("./.env")
    tg_api_token = os.getenv("TG_API_KEY")
    updater = Updater(tg_api_token)
    dispatcher = updater.dispatcher
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(
        MessageHandler(Filters.text & ~Filters.command, reply)
    )
    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
