import random


def set_value_to_redis(redis_conn, _key, _value) -> None:
    redis_conn.set(_key, _value)


def get_value_from_redis(redis_conn, _key) -> str:
    value = redis_conn.get(_key)
    if value:
        return value.decode("utf-8")


def get_new_question_and_answer(_questions):
    _question, _answer = random.choice(list(_questions.items()))
    return _question, _answer


def load_questions(questions_paths):
    questions = {}

    for question_path in questions_paths:
        with open(question_path, encoding="KOI8-R") as file:
            file_content = file.read()
            file_content_split = file_content.split("\n\n")

            for line_index, line in enumerate(file_content_split):
                key = line.split("\n")[0]
                if key.startswith("Вопрос"):
                    question = "\n".join(file_content_split[line_index].split("\n")[1:])
                    answer = "\n".join(file_content_split[line_index + 1].split("\n")[1:])
                    questions[question] = answer

    return questions
