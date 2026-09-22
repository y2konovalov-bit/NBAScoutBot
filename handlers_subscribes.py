from keyboards import teams_keyboard, subscribe_teams_keyboard, main_menu, favorites_teams
from states import SubscribeStates
from storage import delete_user_team, load_user_teams, add_user_team


def register_subscribe_handlers(bot):
    @bot.message_handler(func=lambda message: message.text == 'Подписаться')
    def handle_subscribe_start(message):
        bot.set_state(message.from_user.id, SubscribeStates.choose_team, message.chat.id)
        bot.send_message(
            message.chat.id, 
            'На какую команду подписаться?', 
            reply_markup=subscribe_teams_keyboard())

    @bot.callback_query_handler(
        func=lambda call: call.data.startswith('sub_team:'),
        state=SubscribeStates.choose_team
    )
    def handle_choose_team(callback):
        team_name = callback.data.split(':')[1]
        added = add_user_team(callback.from_user.id, team_name)

        bot.answer_callback_query(callback.id)
        
        if added:
            text = f'Вы подписались на команду {team_name}⭐'
        else:
            text = f'Вы уже подписаны на команду {team_name}!'
        bot.send_message(callback.message.chat.id, text)
        bot.delete_state(callback.from_user.id, callback.message.chat.id)
        bot.send_message(callback.message.chat.id, reply_markup=main_menu())
        
    @bot.message_handler(state=SubscribeStates.choose_team)
    def handle_wrong_input_subscribe(message):
        bot.send_message(message.chat.id, 'Выберите вариант из клавиатуры!')

    @bot.message_handler(func=lambda m: m.text == 'Мои команды')
    def handle_favorites(message):
        teams = load_user_teams(message.from_user.id)
        if not teams:
            bot.send_message(message.from_user.id, "Подпишитесь на любую команду")
            return 
        bot.send_message(message.from_user.id,
                        f"Вот команды, на которые ты подписан:\n(нажми на команду, чтобы отписаться от нее)",
                        reply_markup=favorites_teams(teams))

    @bot.callback_query_handler(func=lambda call: call.data.startswith('unsub_team:'))
    def handle_unsubscribe(callback):
        team_name = callback.data.split(':')[1]
        deleted = delete_user_team(callback.from_user.id, team_name)

        bot.answer_callback_query(callback.id)
        
        if deleted:
            text = f'Вы отписались от команды {team_name}❌'
        else:
            text = f'Вы не были подписаны на команду {team_name}!'
        bot.send_message(callback.message.chat.id, text)
        bot.delete_state(callback.from_user.id, callback.message.chat.id)
        bot.send_message(callback.message.chat.id, reply_markup=main_menu())
        
    