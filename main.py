import os
import glob
from functools import partial
from dotenv import load_dotenv

from unzip_questions import load_questions
from pathlib import Path
from telegram import Update, ForceReply, ReplyKeyboardMarkup
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext


def start(update: Update, context: CallbackContext) -> None:
    """Send a message when the command /start is issued."""
    user = update.effective_user
    update.message.reply_markdown_v2(
        fr'Hi {user.mention_markdown_v2()}\!',
        reply_markup=ForceReply(selective=True),
    )


def reply(update: Update, context: CallbackContext, questions) -> None:
    custom_keyboard = [["Новый вопрос", 'top-right'],
                       ['bottom-left', 'bottom-right']]

    text_response = "buttons"
    if update.message.text == "Новый вопрос":
        for question, answer in questions.items():
            text_response = question

    reply_markup = ReplyKeyboardMarkup(custom_keyboard)
    update.message.reply_markdown(reply_markup=reply_markup, text=text_response)


def main() -> None:
    """Start the bot."""
    load_dotenv(Path.cwd() / ".env")
    tg_api_token = os.environ["TG_API_KEY"]
    questions_files = glob.glob("./quiz-questions/*.txt")
    questions = load_questions(questions_files)
    updater = Updater(tg_api_token)
    dispatcher = updater.dispatcher
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(
        MessageHandler(Filters.text & ~Filters.command, partial(reply, questions=questions))
    )
    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
