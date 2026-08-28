import telebot
from config import TG_API_TOKEN
from handlers_menu import register_menu_handlers

bot = telebot.TeleBot(TG_API_TOKEN)
register_menu_handlers(bot)

bot.infinity_polling()