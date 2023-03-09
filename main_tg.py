import logging
import os
from functools import partial
# from dotenv import load_dotenv
from pathlib import Path

import quize_lib as ql
import redis
from telegram import ReplyKeyboardMarkup
from telegram.ext import (Updater, CommandHandler, MessageHandler, Filters, RegexHandler,
                          ConversationHandler)

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)

CHOOSING = 1

reply_keyboard = [["Новый вопрос", "Показать текущий вопрос"],
                  ["Показать ответ", 'Сдаться', "/cancel"]]
markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)


def start(bot, update):
    update.message.reply_text(
        fr'Hi {update.message.from_user.first_name}!', reply_markup=markup)
    return CHOOSING


def handle_new_question_request(bot, update, redis_conn, questions):
    new_question, answer = ql.get_new_question_and_answer(questions)
    ql.set_value_to_redis(redis_conn, f"{update.message.from_user.id} question", new_question)
    ql.set_value_to_redis(redis_conn, f"{update.message.from_user.id} answer", answer.replace('"', ''))
    update.message.reply_text(new_question)
    return CHOOSING


def resign(bot, update, redis_conn, questions):
    answer = ql.get_value_from_redis(redis_conn, f"{update.message.from_user.id} answer")
    if not answer:
        update.message.reply_text("Вопрос ещё не задан.")
    else:
        update.message.reply_text(answer)
    new_question, answer = ql.get_new_question_and_answer(questions)
    ql.set_value_to_redis(redis_conn, f"{update.message.from_user.id} question", new_question)
    ql.set_value_to_redis(redis_conn, f"{update.message.from_user.id} answer", answer.replace('"', ''))
    update.message.reply_text(new_question)
    return CHOOSING


def show_question(bot, update, redis_conn):
    question = ql.get_value_from_redis(redis_conn, f"{update.message.from_user.id} question")
    if not question:
        update.message.reply_text("Вопрос ещё не задан.")
    else:
        update.message.reply_text(question)
    return CHOOSING


def show_answer(bot, update, redis_conn):
    answer = ql.get_value_from_redis(redis_conn, f"{update.message.from_user.id} answer")
    if not answer:
        update.message.reply_text("Вопрос ещё не задан.")
    else:
        update.message.reply_text(answer)
    return CHOOSING


def handle_solution_attempt(bot, update, redis_conn):
    answer = ql.get_value_from_redis(redis_conn, f"{update.message.from_user.id} answer")
    if update.message.text == answer:
        text_response = "Правильно! Поздравляю! Для следующего вопроса нажми «Новый вопрос»."
    else:
        text_response = "Неправильно… Попробуешь ещё раз?"
    update.message.reply_text(text_response)
    return CHOOSING


def done(bot, update, redis_conn):
    update.message.reply_text('Пока! Если захочешь начать снова, просто напиши "старт".')
    redis_conn.delete(f"{update.message.from_user.id} question")
    redis_conn.delete(f"{update.message.from_user.id} answer")
    return ConversationHandler.END


def error(bot, update, error):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, error)


def main():
    logger.info("Script started.")
    # load_dotenv(Path.cwd() / ".env")
    tg_api_token = os.environ["TG_API_KEY"]

    questions_files = Path.cwd() / "quiz-questions"
    questions = ql.load_questions(questions_files.glob("*.txt"))

    redis_host = os.environ["REDIS_HOST"]
    redis_port = int(os.environ["REDIS_PORT"])
    redis_password = os.environ["REDIS_PASSWORD"]

    updater = Updater(tg_api_token)
    dp = updater.dispatcher

    redis_conn = redis.Redis(
        host=redis_host,
        port=redis_port,
        password=redis_password)

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start),
                      RegexHandler('^старт$', start)],

        states={
            CHOOSING: [
                RegexHandler('^(Новый вопрос)$', partial(handle_new_question_request,
                                                         redis_conn=redis_conn,
                                                         questions=questions)),
                RegexHandler('^(Показать текущий вопрос)$', partial(show_question, redis_conn=redis_conn)),
                RegexHandler('^(Показать ответ)$', partial(show_answer, redis_conn=redis_conn)),
                RegexHandler('^(Сдаться)$', partial(resign, redis_conn=redis_conn, questions=questions)),
                MessageHandler(Filters.text, partial(handle_solution_attempt, redis_conn=redis_conn))
            ],
        },

        fallbacks=[CommandHandler('cancel', partial(done, redis_conn=redis_conn))]
    )

    dp.add_handler(conv_handler)
    dp.add_error_handler(error)
    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
