from random import choice
import csv


# Функция для непосредственной обработки диалога.
def handle_dialog(request, response, user_storage):
    if request.is_new_session:
        response.set_text('Я буду говорить события из русской истории, а ты напинешь мне их даты.')

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
