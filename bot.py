import telebot
from telebot.storage import StateMemoryStorage
from telebot import custom_filters

from config import TG_API_TOKEN
from handlers_menu import register_menu_handlers
from handlers_schedule import register_schedule_handlers
from handlers_subscribes import register_subscribe_handlers

state_storage = StateMemoryStorage()

bot = telebot.TeleBot(TG_API_TOKEN, state_storage=state_storage)

bot.add_custom_filter(custom_filters.StateFilter(bot))

register_menu_handlers(bot)
register_schedule_handlers(bot)
register_subscribe_handlers(bot)


bot.infinity_polling()