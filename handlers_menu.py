import telebot
from keyboards import main_menu

def register_menu_handlers(bot):
    TEXT_START="Привет! Я NBA Scout - помогу следить за расписанием и любимыми командами."
    TEXT_HELP=f'''
    Вот что я умею:\n
/start - Перезапустить бота\n
/schedule - Расписание матчей лиги\n
/cancel - Выход из любого текущего сценария и возвращение в меню\n
/table, /t - Турнирная таблица NBA\n
/conf - Турнирная таблица конференции\n
/favorite - Команды, за которыми наблюдает пользователь\n
/subscribe - Подписка на команду\n
/unsubscribe - Отписка на команду\n
/stats - Посмотреть статистику игрока\n\n
    Если остались другие вопросы по работе бота - пишите в поддержку: @y2konovalov 
'''
    
    @bot.message_handler(commands=['start'])
    def handle_start(message):
        bot.send_message(message.chat.id,
                          TEXT_START, 
                          reply_markup=main_menu())
    
    @bot.message_handler(commands=['help'])
    def handle_help(message):
        bot.send_message(message.chat.id, TEXT_HELP)

    @bot.message_handler(
        func=lambda msg: msg.text == "Помощь"
    )
    def handle_help(message):
        bot.send_message(message.chat.id, TEXT_HELP)

    @bot.message_handler(commands=['cancel'])
    def handle_cancel(message):
        bot.delete_state(message.from_user.id, message.chat.id)
        bot.send_message(message.chat.id, "Вы вышли в главное меню", reply_markup=main_menu())
        


