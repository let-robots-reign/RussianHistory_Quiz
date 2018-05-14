from random import choice, shuffle
import csv
from itertools import cycle


with open("russian-history-events.csv", "r", encoding="utf8") as csvfile:
    data = csv.DictReader(csvfile, delimiter=",", quotechar=" ")
    events = {x["event"]: x["year"] for x in data}


# Функция для непосредственной обработки диалога.
def handle_dialog(request, response, user_storage):
    if request.is_new_session:
        user_storage = {}
        _a = list(events.keys())
        shuffle(_a)
        inf_list = cycle(_a)
        user_storage['questions'] = inf_list

        event = next(user_storage['questions'])
        year = events[event]
        buttons = get_random_buttons(year)

        user_storage["event"] = event
        user_storage["answer"] = year
        user_storage["buttons"] = buttons
        user_storage["right_answers"] = 0
        response.set_text('Я буду говорить события из русской истории, а ты напишешь мне их даты.\n'
                          'Для завершения игры скажите "конец игры".\n'
                          'Скажи, когда произошло: {}'.format(user_storage["event"]))
        response.set_buttons(user_storage["buttons"])

        return response, user_storage

    else:
        # Обрабатываем ответ пользователя.
        if request.command.lower() == "конец игры":
            response.set_text("Спасибо за игру!\n Правильных ответов: {}\n".format(user_storage["right_answers"])
                              + "До встречи!")
            response.set_end_session(True)
            user_storage = {}

            return response, user_storage

        elif request.command.lower() == user_storage["answer"]:
            # Пользователь ввел правильный вариант ответа.
            event = next(user_storage['questions'])
            year = events[event]
            buttons = get_random_buttons(year)
            user_storage["event"] = event
            user_storage["answer"] = year
            user_storage["buttons"] = buttons
            user_storage["right_answers"] += 1
            response.set_text('Верно!\n'
                              'Следующий вопрос: когда произошло событие: {}'.format(user_storage["event"]))
            response.set_buttons(user_storage["buttons"])

            return response, user_storage

        buttons = get_random_buttons(user_storage['answer'])

        response.set_buttons(buttons)
        response.set_text("Неверно! Попробуй еще раз.")

        return response, user_storage


def get_random_buttons(date):
    dates = list(range(800, 2000))
    dates.pop(dates.index(int(date)))
    shuffle(dates)

    dates = dates[:3]
    dates.append(date)
    shuffle(dates)
    buttons = [{'title': str(date), 'hide': True} for date in dates]

    return buttons

