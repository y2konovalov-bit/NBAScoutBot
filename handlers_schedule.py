from keyboards import main_menu, teams_keyboard, schedule_type_keyboard, main_menu
from states import SheduleStates
from api_games import get_games
from teams import TEAM_IDS


def format_games(games, team_name):
    lines = [f'Матчи команды {team_name}:']
    for game in games:
        if game['score'] is None:
            lines.append(f"• {game['date']} — против {game['opponent']}")
        else:
            lines.append(
                f"• {game['date']} — против {game['opponent']}, "
                f"счёт: {game['score']}")
    return "\n".join(lines)

def register_schedule_handlers(bot):
    @bot.message_handler(func=lambda message: message.text == 'Расписание')
    def handle_schedule_start(message):
        bot.set_state(message.from_user.id, SheduleStates.choose_team, message.chat.id)
        bot.send_message(message.chat.id, "Выберите команду", reply_markup=teams_keyboard())

    @bot.callback_query_handler(
        func=lambda call: call.data.startswith('team:'),
        state=SheduleStates.choose_team
    )
    def handle_choose_team(callback):
        team_name = callback.data.split(':')[1]

        with bot.retrieve_data(callback.from_user.id, callback.message.chat.id) as data:
            data['team'] = team_name

        bot.set_state(callback.from_user.id, SheduleStates.choose_type, callback.message.chat.id)
        bot.answer_callback_query(callback.id)
        bot.send_message(
            callback.message.chat.id,
            f"Вы выбрали команду: {team_name}. Теперь выберите тип расписания.",
            reply_markup=schedule_type_keyboard()
        )

    @bot.callback_query_handler(
        func=lambda call: call.data.startswith('games:'),
        state=SheduleStates.choose_type
    )
    def handle_choose_type(callback):
        schedule_type = callback.data.split(':')[1]

        with bot.retrieve_data(callback.from_user.id, callback.message.chat.id) as data:
            team_name = data.get('team', 'Команда')

        team_id = TEAM_IDS.get(team_name)
        games = get_games(team_id, schedule_type)

        if games is None:
            text = f'Сервис перегружен, повторите попытку чуть позже'
        elif not games:
            text = f'Для команды {team_name} не было найдено ни одной игры'
        else:
            text = format_games(games, team_name)

        bot.answer_callback_query(callback.id)
        bot.send_message(callback.message.chat.id, text)

        bot.delete_state(callback.from_user.id, callback.message.chat.id)
        bot.send_message(
            callback.message.chat.id,
            'Главное меню',
            reply_markup=main_menu(),
        )

    @bot.message_handler(
        func=lambda message: True,
        state=SheduleStates.choose_team,
    )
    def handle_invalid_text_choose_team(message):
        bot.send_message(
            message.chat.id,
            'Пожалуйста, выберите команду с помощью кнопок, а не текстом.',
            reply_markup=teams_keyboard(),
        )

    @bot.message_handler(
        func=lambda message: True,
        state=SheduleStates.choose_type,
    )
    def handle_invalid_text_choose_type(message):
        bot.send_message(
            message.chat.id,
            'Пожалуйста, выберите тип расписания с помощью кнопок.',
            reply_markup=schedule_type_keyboard(),
        )