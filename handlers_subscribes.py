import json
import os
from keyboards import teams_keyboard, confirmation_keyboard, main_menu
from states import SubscribeStates

SUBSCRIPTIONS_FILE = 'subscriptions.json'
def register_subscribe_handlers(bot):
    @bot.message_handler(func=lambda message: message.text == 'Подписаться')
    def handle_subscribe_start(message):
        bot.set_state(message.from_user.id, SubscribeStates.choose_team, message.chat.id)
        bot.send_message(message.chat.id, 'Выберите команду', reply_markup=teams_keyboard())

    @bot.callback_query_handler(
        func=lambda call: call.data.startswith('team:'),
        state=SubscribeStates.choose_team
    )
    def handle_choose_team(callback):
        team_name = callback.data.split(':')[1]

        with bot.retrieve_data(callback.from_user.id, callback.message.chat.id) as data:
            data['team'] = team_name

        bot.set_state(callback.from_user.id, SubscribeStates.confirmation, callback.message.chat.id)
        bot.answer_callback_query(callback.id)
        bot.send_message(
            callback.message.chat.id,
            f'Вы выбрали команду: {team_name}.\n\n Вы уверены, что хотите подписаться на эту команду?',
            reply_markup=confirmation_keyboard()
        )

    @bot.callback_query_handler(
            func= lambda call: call.data.startswith('confirmation:'),
            state=SubscribeStates.confirmation)
    def handle_confirmation(callback):
        confirmation_answer = callback.data.split(':')[1]
        user_id = callback.from_user.id
        chat_id = callback.message.chat.id

        if confirmation_answer == 'confirm':
            with bot.retrieve_data(user_id, chat_id) as data:
                team_name = data.get('team')
            if not team_name:
                bot.answer_callback_query(callback.id, 'Ошибка, попробуйте снова.')
                bot.send_message(chat_id, 'Не удалось определить команду', reply_markup = main_menu())
                bot.delete_state(user_id, chat_id)
                return
            subs = {}
            if os.path.exists(SUBSCRIPTIONS_FILE):
                try:
                    with open(SUBSCRIPTIONS_FILE, "r", encoding='utf-8') as f:
                        subs = json.load(f)
                except (json.JSONDecodeError, IOError):
                    subs = {}

            uid = str(user_id)
            if uid not in subs:
                subs[uid] = []

            if team_name in subs[uid]:
                bot.answer_callback_query(callback.id, '⚠️ Вы уже подписаны на эту команду.')
                bot.send_message(chat_id, f'Вы уже подписаны на {team_name}.', reply_markup=main_menu())
            else:
                subs[uid].append(team_name)
                with open (SUBSCRIPTIONS_FILE, "w", encoding="utf-8") as f:
                    json.dump(subs, f, ensure_ascii=False, indent=2)
                bot.answer_callback_query(callback.id, f'✅ Подписка на {team_name} оформлена!')
                bot.send_message(
                    chat_id,
                    f'Вы подписались на новости команды: {team_name}!',
                    reply_markup=main_menu()
                )
            bot.delete_state(user_id, chat_id)

        elif confirmation_answer == 'cancel':
            bot.answer_callback_query(callback.id, 'Процесс подписки отменен.')
            bot.delete_state(user_id, chat_id)
            bot.send_message(
                chat_id,
                "Вы вернулись в главное меню.",
                reply_markup=main_menu()
            )