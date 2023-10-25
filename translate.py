from aiogram.utils import executor
from create_bot import dp
from handlers import client, admin, other
from data_base import sqlite_bd
from aiogram.utils import executor

async def on_startup(_):
    print('OK')
    sqlite_bd.sql_start()

client.register_handlers_client(dp)

executor.start_polling(dp, skip_updates=True, on_startup=on_startup)