from keyboards import main_menu, teams_keyboard, schedule_type_keyboard
from states import SheduleStates

MOCK_GAMES = {
    "upcoming": [
        {"date": "2026-09-10", "opponent": "Celtics"},
        {"date": "2026-09-14", "opponent": "Warriors"},
    ],
    "past": [
        {"date": "2026-08-28", "opponent": "Bulls", "score": "110:102"},
        {"date": "2026-08-25", "opponent": "Heat", "score": "98:101"},
    ],
}

def format_upcoming(games):
    lines = ['Предстоящие матчи:']
    for g in games:
        lines.append(f" {g['date']} — {g['opponent']}")
    return "\n".join(lines)

def format_past(games):
    lines = ["Прошедшие матчи:"]
    for g in games:
        lines.append(f" {g['date']} — {g['opponent']} ({g['score']})")
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

        games = MOCK_GAMES.get(schedule_type, [])

        if schedule_type == 'upcoming':
            text = f'Команда: {team_name} \n\n' + format_upcoming(games)
        elif schedule_type == 'past':
            text = f'Команда: {team_name} \n\n' + format_past(games)
        else:
            text = 'Неизвестный тип расписания'

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