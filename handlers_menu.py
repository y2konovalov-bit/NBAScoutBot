import telebot
from keyboards import main_menu

def register_menu_handlers(bot):
    @bot.message_handler(commands=['start'])
    def handle_start(message):
        bot.send_message(message.chat.id,
                          'Привет! Я NBA Scout - помогу следить за расписанием и любимыми командами.', 
                          reply_markup=main_menu())
    
    @bot.message_handler(commands=['help'])
    def handle_help(message):
        bot.send_message(message.chat.id, 'Вот что я умею:\n/schedule — расписание\n...')
