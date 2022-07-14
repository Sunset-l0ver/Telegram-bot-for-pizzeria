from aiogram import Bot
from aiogram.dispatcher import Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage


BOT_TOKEN = "5367036604:AAHEZvXO7nOGZcysWgsOSF52MWaPndepAHk"
ADMINS = ["1547396618", ]


storage = MemoryStorage()


bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(bot, storage=storage)
