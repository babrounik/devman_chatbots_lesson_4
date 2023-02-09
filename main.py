from telegram import ReplyKeyboardMarkup
from telegram.ext import (Updater, CommandHandler, MessageHandler, Filters, RegexHandler,
                          ConversationHandler)

import random
import logging
import os
from dotenv import load_dotenv
from pathlib import Path

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)

CHOOSING, TYPING_REPLY, TYPING_CHOICE = range(3)

reply_keyboard = [["Новый вопрос", "Показать текущий вопрос"],
                  ["Показать ответ", "Закончить"]]
markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)


def set_value_to_redis(redis_conn, _key, _value) -> None:
    redis_conn.set(_key, _value)


def get_value_from_redis(redis_conn, _key) -> str:
    return redis_conn.get(_key).decode("utf-8")


def get_new_question_and_answer(_questions):
    _question, _answer = random.choice(list(_questions.items()))
    return _question, _answer


def start(bot, update):
    update.message.reply_text(
        fr'Hi {update.effective_user.mention_markdown_v2()}\!',
        reply_markup=markup)

    return CHOOSING


def handle_new_question_request(bot, update, _redis_conn, _questions):
    new_question, answer = get_new_question_and_answer(_questions)
    set_value_to_redis(_redis_conn, f"{update.message.from_user.id} question", new_question)
    set_value_to_redis(_redis_conn, f"{update.message.from_user.id} answer", answer.replace('"', ''))
    update.message.reply_text(new_question)
    return TYPING_REPLY


def show_question(bot, update, _redis_conn):
    question = get_value_from_redis(_redis_conn, f"{update.message.from_user.id} question")
    update.message.reply_text(question)
    return TYPING_REPLY


def show_answer(bot, update, _redis_conn):
    question = get_value_from_redis(_redis_conn, f"{update.message.from_user.id} answer")
    update.message.reply_text(question)
    return TYPING_REPLY


def handle_solution_attempt(bot, update, _redis_conn):
    answer = get_value_from_redis(_redis_conn, f"{update.message.from_user.id} answer")
    if update.message.text == answer:
        text_response = "Правильно! Поздравляю! Для следующего вопроса нажми «Новый вопрос»."
    else:
        text_response = "Неправильно… Попробуешь ещё раз?"
    update.message.reply_text(text_response)
    return CHOOSING


def done(bot, update):
    update.message.reply_text('Пока! Если захочешь начать снова, просто напиши "старт".')
    return ConversationHandler.END


def error(bot, update, error):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, error)


def main():
    load_dotenv(Path.cwd() / ".env")
    tg_api_token = os.environ["TG_API_KEY"]
    updater = Updater(tg_api_token)
    dp = updater.dispatcher

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start),
                      RegexHandler('^старт$', start)],

        states={
            CHOOSING: [
                RegexHandler('^(Новый вопрос)$', handle_new_question_request),
                RegexHandler('^(Показать текущий вопрос)$', show_question),
                RegexHandler('^(Показать ответ)$', show_answer),
                MessageHandler(Filters.text, handle_solution_attempt)
            ],

            TYPING_REPLY: [MessageHandler(Filters.text, handle_solution_attempt)],
        },

        fallbacks=[RegexHandler('^Закончить$', done, pass_user_data=True)]
    )

    dp.add_handler(conv_handler)
    dp.add_error_handler(error)
    updater.start_polling()
    updater.idle()

    if __name__ == '__main__':
        main()
