import vk_api
from vk_api.keyboard import VkKeyboard, VkKeyboardColor
from vk_api.longpoll import VkLongPoll, VkEventType
from vk_api.utils import get_random_id

import logging
import os
from dotenv import load_dotenv
from pathlib import Path

import quize_lib as ql
import redis

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)

keyboard = VkKeyboard(one_time=True)
keyboard.add_button("Новый вопрос", color=VkKeyboardColor.SECONDARY)
keyboard.add_button("Показать текущий вопрос", color=VkKeyboardColor.POSITIVE)

keyboard.add_line()
keyboard.add_button("Показать ответ", color=VkKeyboardColor.NEGATIVE)
keyboard.add_button('Сдаться', color=VkKeyboardColor.PRIMARY)
keyboard.add_button("/cancel", color=VkKeyboardColor.NEGATIVE)


def start():
    vk.messages.send(
        peer_id=212875594,
        random_id=get_random_id(),
        keyboard=keyboard.get_keyboard(),
        message='Пример клавиатуры'
    )


def handle_new_question_request():
    pass


def show_question():
    pass


def show_answer():
    pass


def resign():
    pass


def done():
    pass


def handle_solution_attempt():
    pass


def main():
    """ Пример создания клавиатуры для отправки ботом """
    env_file = Path.cwd() / ".env"
    load_dotenv(env_file)
    vk_token = os.environ["VK_COM"]

    vk_session = vk_api.VkApi(token=vk_token)
    vk = vk_session.get_api()

    longpoll = VkLongPoll(vk_session)
    for event in longpoll.listen():
        if event.type == VkEventType.MESSAGE_NEW and event.to_me:
            if event.text == "Начать":
                start()
            elif event.text == "Новый вопрос":
                handle_new_question_request()
            elif event.text == "Показать текущий вопрос":
                show_question()
            elif event.text == "Показать ответ":
                show_answer()
            elif event.text == 'Сдаться':
                resign()
            elif event.text == "/cancel":
                done()
            else:
                handle_solution_attempt()
            # reply(event, vk_api, project_id, language_code)


if __name__ == '__main__':
    main()
