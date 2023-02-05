import os
import glob
import random
from functools import partial
from dotenv import load_dotenv

import redis
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


def reply(update: Update, context: CallbackContext, questions, redis_conn) -> None:
    custom_keyboard = [["Новый вопрос", 'Показать текущий вопрос'],
                       ['Показать ответ', 'bottom-right']]

    text_response = "buttons"
    if update.message.text == "Новый вопрос":
        question, _ = random.choice(list(questions.items()))
        text_response = question
        redis_conn.set(update.effective_user.id, question)
    elif update.message.text == 'Показать текущий вопрос':
        question = redis_conn.get(update.effective_user.id).decode("utf-8")
        text_response = question
    elif update.message.text == 'Показать ответ':
        question = redis_conn.get(update.effective_user.id).decode("utf-8")
        answer = questions.get(question).replace('"', '')
        text_response = answer
    else:
        question = redis_conn.get(update.effective_user.id).decode("utf-8")
        answer = questions.get(question).replace('"', '')
        if update.message.text == answer:
            text_response = "Правильно! Поздравляю! Для следующего вопроса нажми «Новый вопрос»"
        else:
            text_response = "Неправильно… Попробуешь ещё раз?"

    reply_markup = ReplyKeyboardMarkup(custom_keyboard)
    update.message.reply_markdown(reply_markup=reply_markup, text=text_response)


def main() -> None:
    """Start the bot."""
    load_dotenv(Path.cwd() / ".env")
    tg_api_token = os.environ["TG_API_KEY"]
    redis_host = os.environ["REDIS_HOST"]
    redis_port = int(os.environ["REDIS_PORT"])
    redis_password = os.environ["REDIS_PASSWORD"]

    redis_conn = redis.Redis(
        host=redis_host,
        port=redis_port,
        password=redis_password)

    questions_files = glob.glob("./quiz-questions/*.txt")
    questions = load_questions(questions_files)
    updater = Updater(tg_api_token)
    dispatcher = updater.dispatcher
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(
        MessageHandler(Filters.text & ~Filters.command, partial(reply, questions=questions, redis_conn=redis_conn))
    )
    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
