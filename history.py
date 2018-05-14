from random import choice,shuffle
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
        user_storage["event"] = event
        user_storage["answer"] = year

        response.set_text('Я буду говорить события из русской истории, а ты напишешь мне их даты.\n'
                          'Скажи, когда произошло: {}'.format(event))

        return response, user_storage

    else:

        if "event" not in user_storage.keys():
            event = choice(list(events.keys()))
            year = events[event]
            user_storage["event"] = event
            user_storage["answer"] = year
        else:
            event = user_storage["event"]
            year = user_storage["answer"]

        # Обрабатываем ответ пользователя.
        if request.command.lower() == year:
            # Пользователь ввел правильный вариант ответа.
            event = next(user_storage['questions'])
            year = events[event]
            user_storage["event"] = event
            user_storage["answer"] = year
            response.set_text('Верно!\n'
                              'Следующий вопрос: когда произошло событие: {}'.format(event))

            return response, user_storage

        response.set_text("Неверно! Попробуй еще раз.")

        return response, user_storage
