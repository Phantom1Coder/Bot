from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
import os
from aiogram.contrib.fsm_storage.memory import MemoryStorage

storage = MemoryStorage()

TOKEN = ('6428286075:AAHhlIqQN1sTQQ7_cn_SWCWnyK5xOqWmW5o')
async def on_startup(dp):
    await bot.send_message(chat_id=1, text="Бот запущен")
bot = Bot(token = TOKEN)
dp = Dispatcher(bot, storage=storage)

