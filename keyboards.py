from telebot import types
from teams import TEAM_NAMES

def main_menu():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add('Расписание', 'Мои команды')
    markup.add('Подписаться', 'Таблица')
    markup.add('Статистика игрока', 'Помощь')
    return markup

def teams_keyboard():
    markup = types.InlineKeyboardMarkup(row_width=2)
    buttons = [
        types.InlineKeyboardButton(team, callback_data=f'team:{team}') 
        for team in TEAM_NAMES
    ]
    markup.add(*buttons)
    return markup


def schedule_type_keyboard():
    markup = types.InlineKeyboardMarkup(row_width=1)
    markup.add(types.InlineKeyboardButton('Ближайшие игры', callback_data='games:upcoming'), # общая_часть:индивидуальная_часть
               types.InlineKeyboardButton('Прошедшие игры', callback_data='games:past'))
    return markup

def subscribe_teams_keyboard():
    markup = types.InlineKeyboardMarkup(row_width=2)
    buttons = [
        types.InlineKeyboardButton(team, callback_data=f'sub_team:{team}') 
        for team in TEAM_NAMES
    ]
    markup.add(*buttons)
    return markup

def favorites_teams(team_names):
    markup = types.InlineKeyboardMarkup(row_width=2)
    buttons = [
        types.InlineKeyboardButton(f'❌{team}', callback_data=f'unsub_team:{team}') 
        for team in team_names
    ]
    markup.add(*buttons)
    return markup
