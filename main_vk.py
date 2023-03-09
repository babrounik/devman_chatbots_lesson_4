import vk_api
from vk_api.keyboard import VkKeyboard, VkKeyboardColor
from vk_api.longpoll import VkLongPoll, VkEventType
from vk_api.utils import get_random_id

import logging
import os
from pathlib import Path

import quize_lib as ql
import redis

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)

keyboard = VkKeyboard(one_time=True)
keyboard.add_button("Новый вопрос", color=VkKeyboardColor.SECONDARY)
keyboard.add_button("Показать текущий вопрос", color=VkKeyboardColor.SECONDARY)

keyboard.add_line()
keyboard.add_button("Показать ответ", color=VkKeyboardColor.SECONDARY)
keyboard.add_button('Сдаться', color=VkKeyboardColor.NEGATIVE)


def start(_vk, _event):
    _vk.messages.send(
        peer_id=_event.user_id,
        random_id=get_random_id(),
        keyboard=keyboard.get_keyboard(),
        message=fr'Привет! Нажми "Новый вопрос", чтобы приступить к викторине.'
    )


def handle_new_question_request(_vk, _event, _redis_conn, _questions):
    new_question, answer = ql.get_new_question_and_answer(_questions)
    ql.set_value_to_redis(_redis_conn, f"{_event.user_id} question", new_question)
    ql.set_value_to_redis(_redis_conn, f"{_event.user_id} answer", answer.replace('"', ''))

    _vk.messages.send(
        peer_id=_event.user_id,
        random_id=get_random_id(),
        keyboard=keyboard.get_keyboard(),
        message=new_question
    )


def show_question(_vk, _event, _redis_conn):
    question = ql.get_value_from_redis(_redis_conn, f"{_event.user_id} question")
    if not question:
        _vk.messages.send(
            peer_id=_event.user_id,
            random_id=get_random_id(),
            keyboard=keyboard.get_keyboard(),
            message="Вопрос ещё не задан."
        )
    else:
        _vk.messages.send(
            peer_id=_event.user_id,
            random_id=get_random_id(),
            keyboard=keyboard.get_keyboard(),
            message=question
        )


def show_answer(_vk, _event, _redis_conn):
    answer = ql.get_value_from_redis(_redis_conn, f"{_event.user_id} answer")
    if not answer:
        _vk.messages.send(
            peer_id=_event.user_id,
            random_id=get_random_id(),
            keyboard=keyboard.get_keyboard(),
            message="Вопрос ещё не задан."
        )
    else:
        _vk.messages.send(
            peer_id=_event.user_id,
            random_id=get_random_id(),
            keyboard=keyboard.get_keyboard(),
            message=answer
        )


def resign(_vk, _event, _redis_conn, _questions):
    answer = ql.get_value_from_redis(_redis_conn, f"{_event.user_id} answer")
    if not answer:
        _vk.messages.send(
            peer_id=_event.user_id,
            random_id=get_random_id(),
            keyboard=keyboard.get_keyboard(),
            message="Вопрос ещё не задан."
        )
    else:
        _vk.messages.send(
            peer_id=_event.user_id,
            random_id=get_random_id(),
            keyboard=keyboard.get_keyboard(),
            message=answer
        )

    new_question, answer = ql.get_new_question_and_answer(_questions)
    ql.set_value_to_redis(_redis_conn, f"{_event.user_id} question", new_question)
    ql.set_value_to_redis(_redis_conn, f"{_event.user_id} answer", answer.replace('"', ''))

    _vk.messages.send(
        peer_id=_event.user_id,
        random_id=get_random_id(),
        keyboard=keyboard.get_keyboard(),
        message=new_question
    )


def handle_solution_attempt(_vk, _event, _redis_conn):
    answer = ql.get_value_from_redis(_redis_conn, f"{_event.user_id} answer")
    if _event.text == answer:
        text_response = "Правильно! Поздравляю! Для следующего вопроса нажми «Новый вопрос»."
    else:
        text_response = "Неправильно… Попробуешь ещё раз?"
    _vk.messages.send(
        peer_id=_event.user_id,
        random_id=get_random_id(),
        keyboard=keyboard.get_keyboard(),
        message=text_response
    )


def main():
    logger.info("Script started.")

    questions_files = Path.cwd() / "quiz-questions"
    questions = ql.load_questions(questions_files.glob("*.txt"))

    redis_host = os.environ["REDIS_HOST"]
    redis_port = int(os.environ["REDIS_PORT"])
    redis_password = os.environ["REDIS_PASSWORD"]

    redis_conn = redis.Redis(
        host=redis_host,
        port=redis_port,
        password=redis_password)

    vk_token = os.environ["VK_COM"]

    vk_session = vk_api.VkApi(token=vk_token)
    vk = vk_session.get_api()

    longpoll = VkLongPoll(vk_session)
    for event in longpoll.listen():
        if event.type == VkEventType.MESSAGE_NEW and event.to_me:
            if event.text == "Начать":
                start(vk, event)
            elif event.text == "Новый вопрос":
                handle_new_question_request(vk, event, redis_conn, questions)
            elif event.text == "Показать текущий вопрос":
                show_question(vk, event, redis_conn)
            elif event.text == "Показать ответ":
                show_answer(vk, event, redis_conn)
            elif event.text == 'Сдаться':
                resign(vk, event, redis_conn, questions)
            else:
                handle_solution_attempt(vk, event, redis_conn)


if __name__ == '__main__':
    main()
