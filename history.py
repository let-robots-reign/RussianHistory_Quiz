# coding: utf-8
from __future__ import unicode_literals
import csv
import random


with open("russian-history-events.csv", "r", encoding="utf8") as csvfile:
    data = csv.DictReader(csvfile, delimiter=",", quotechar=" ")
    print(list(data))


# Функция для непосредственной обработки диалога.
def handle_dialog(request, response, user_storage):
    if request.is_new_session:
        response.set_text('Привет! Купи слона!')
        response.set_buttons(buttons)

        return response, user_storage

    # Обрабатываем ответ пользователя.
    if request.command.lower() in ['ладно', 'куплю', 'покупаю', 'хорошо']:
        # Пользователь согласился, прощаемся.
        response.set_text('Слона можно найти на Яндекс.Маркете!')

        return response, user_storage

    # Если нет, то убеждаем его купить слона!
    buttons, user_storage = get_suggests(user_storage)
    response.set_text('Все говорят "{}", а ты купи слона!'.format(request.command))
    response.set_buttons(buttons)

    return response, user_storage


# Функция возвращает две подсказки для ответа.
def get_suggests(user_storage):
    # Выбираем две первые подсказки из массива.
    suggests = [
        {'title': suggest, 'hide': True}
        for suggest in user_storage['suggests'][:2]
    ]

    # Убираем первую подсказку, чтобы подсказки менялись каждый раз.
    user_storage['suggests'] = user_storage['suggests'][1:]

    # Если осталась только одна подсказка, предлагаем подсказку
    # со ссылкой на Яндекс.Маркет.
    if len(suggests) < 2:
        suggests.append({
            "title": "Ладно",
            "url": "https://market.yandex.ru/search?text=слон",
            "hide": True
        })

    return suggests, user_storage

