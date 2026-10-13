from keyboards import main_menu
from states import PlayerStates
from api_stats import get_player_stats, find_player


def register_player_handlers(bot):
    @bot.message_handler(func=lambda m: m.text == "Статистика игрока")
    def handle_player_start(message):
        bot.set_state(message.from_user.id, PlayerStates.entering_name, message.chat.id)
        bot.send_message(message.chat.id, "Введите имя или фамилию игрока: ")

    @bot.message_handler(state=PlayerStates.entering_name)
    def handler_player_search(message):
        name = message.text.strip()

        if len(name) < 2:
            bot.send_message(message.chat.id, "Имя должно содержать хотя бы 2 символа")
            return

        player_id = find_player(name)
        if player_id is None:
            bot.send_message(message.chat.id, f"Игрок {name} не найден")
        else:
            stats = get_player_stats(player_id, season=2024)
            if stats is None:
                bot.send_message(message.chat.id, "Не удалось получить статистику игрока")
            else:
                lines = [
                    f"Статистика игрока {name}:",
                    f"Очки: {stats.get('points', 0)}",
                    f"Подборы: {stats.get('rebounds', 0)}",
                    f"Передачи: {stats.get('assists', 0)}",
                    f"Сыграно: {stats.get('games_played', 0)}",  
                ]
                bot.send_message(message.chat.id, "\n".join(lines))

        bot.delete_state(message.from_user.id, message.chat.id)
        bot.send_message(message.chat.id, "Вы вернулись в главное меню", reply_markup=main_menu())

    @bot.message_handler(commands=['cancel'], state=PlayerStates.entering_name)
    def handle_cancel_player(message):
        bot.delete_state(message.from_user.id, message.chat.id)
        bot.send_message(message.chat.id, "Вы вернулись в главное меню", reply_markup=main_menu())