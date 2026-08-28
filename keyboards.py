from telebot import types

def main_menu():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add('Расписание', 'Мои команды')
    markup.add('Подписаться', 'Таблица')
    markup.add('Статистика игрока', 'Помощь')
    return markup