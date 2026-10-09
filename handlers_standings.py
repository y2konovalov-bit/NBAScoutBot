from keyboards import standings_view_keyboard, main_menu
from states import StandingsStates
from api_stats import get_standings


def register_standings_handlers(bot):
    @bot.message_handler(func=lambda message: message.text == 'Таблица')
    def handle_standings_start(message):
        bot.set_state(message.from_user.id, StandingsStates.choose_view, message.chat.id)
        bot.send_message(
            message.chat.id, 
            'Какую таблицу показать?', 
            reply_markup=standings_view_keyboard())

    @bot.callback_query_handler(
        func=lambda call: call.data.startswith('standings:'),
        state=StandingsStates.choose_view
    )
    def handle_standings_view(callback):
        view_type = callback.data.split(':')[1]
        standings = get_standings(view_type)

        bot.answer_callback_query(callback.id)

        if standings is None:
            bot.send_message(callback.message.chat.id, "Не получилось получить данныеб попробуйте позже")
        elif not standings:
            bot.send_message(callback.message.chat.id, "Нет данных")
        else:
            lines = ['Турнирная таблица NBA:']
            for i, team in enumerate(standings, 1):
                w = team['wins']
                l = team['losses']
                lines.append(f"{i}. {team['name']} --- {w} побед, {l} поражений")
            bot.send_message(callback.message.chat.id, '\n'.join(lines))
        bot.delete_state(callback.from_user.id, callback.message.chat.id)
        bot.send_message(callback.message.chat.id, 'Главное меню:', reply_markup=main_menu())
                
    @bot.message_handler(state=StandingsStates.choose_view)
    def handle_wrong_input_subscribe(message):
        bot.send_message(message.chat.id, 'Выберите вариант из клавиатуры!')