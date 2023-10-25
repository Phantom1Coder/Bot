from aiogram import types, Dispatcher
from create_bot import dp, Bot
from keyboards import kb_client, language
from data_base import sqlite_bd
from aiogram.dispatcher import FSMContext
import datetime
from aiogram.dispatcher.filters import Command
from googletrans import Translator
import sqlite3
from aiogram import types
admin_id = 1376076911

@dp.message_handler(commands=['get_id'])
async def get_user_id(message: types.Message):
    if len(message.text.split()) != 2:
        await message.reply("Использование: /get_id <username>")
        return
    
    username = message.text.split()[1]
    
    user_id = sqlite_bd.get_user_id_by_username(username)
    
    if user_id:
        await message.reply(f"ID пользователя с ником {username}: {user_id}")
    else:
        await message.reply("Пользователь не найден")

@dp.message_handler(commands=['set_status'])
async def set_user_status(message: types.Message):
    telegram_id = message.from_user.id
    
    user_info = sqlite_bd.is_user_in_db(telegram_id)
    if user_info:
        user_status = user_info[0]
        if user_status == '2':  # Проверка статуса пользователя
            try:
                target_user_id, new_status = map(int, message.get_args().split())
            except ValueError:
                await message.reply("Использование: /set_status <id_пользователя> <статус>")
                return
            
            target_user = sqlite_bd.is_user_in_db(target_user_id)
            if target_user:
                sqlite_bd.cur.execute("UPDATE users SET status=? WHERE telegram_id=?", (new_status, target_user_id))
                sqlite_bd.base.commit()
                await message.reply(f"Статус пользователя с ID {target_user_id} обновлен на {new_status}")
            else:
                await message.reply(f"Пользователь с ID {target_user_id} не найден в базе данных")
        else:
            await message.reply("У вас нет доступа к этой команде")
    else:
        await message.reply("Вы не зарегистрированы в базе данных. Введите команду /start для регистрации.")

@dp.message_handler(commands=['start'])
async def comm_start(message: types.Message):
    telegram_id = message.from_user.id
    user_info = sqlite_bd.is_user_in_db(telegram_id)  # Проверка наличия пользователя в базе данных
    
    if user_info is not None:
        if user_info[0] != '0':
            await message.reply("Для перевода воспользуйтесь кнопками ниже.", reply_markup=kb_client)
        else:
            await message.reply("Извините, у вас нет доступа к использованию бота.")
    else:
        username = message.from_user.username
        date_reg = datetime.datetime.today().strftime("%Y-%m-%d")
        sqlite_bd.add_user(username, telegram_id, date_reg)  # Используйте функцию add_user для добавления пользователя
        await message.from_user.id("Вас приветствует Бот-Переводчик! Ваш Telegram ID был добавлен в базу данных.", reply_markup=kb_client)

@dp.message_handler(commands=['help'])
async def comm_help(message: types.Message):
  telegram_id = message.from_user.id
  user_info = sqlite_bd.is_user_in_db(telegram_id)
    
  if user_info is not None:
        if user_info[0] != '0':
            # Здесь можно вывести кнопки или текст команды /help
            await message.reply("Это помощь. Вот что вы можете делать с этим ботом: ...")
        else:
            await message.reply("Извините, у вас нет доступа к использованию бота.")
  else:
        await message.reply("Вы не зарегистрированы в базе данных. Введите команду /start для регистрации.") 


@dp.message_handler(commands=['Перевод'])
async def comm_trans(message: types.Message):
    telegram_id = message.from_user.id
    user_info = sqlite_bd.is_user_in_db(telegram_id)

    if user_info is not None:
        if user_info[0] != '0':
            await message.reply("Введите текст, который вы хотите перевести:")
        else:
            await message.reply("Извините, у вас нет доступа к использованию бота.")
    else:
        await message.reply("Вы не зарегистрированы в базе данных. Введите команду /start для регистрации.")

def register_handlers_client(dp : Dispatcher):
    dp.register_message_handler(comm_start, commands=['start'])
    dp.register_message_handler(comm_help, commands=['help'])

@dp.message_handler(commands=['Menu'])
async def personal_cabinet(message: types.Message):
    # Получаем информацию о пользователе из базы данных
    telegram_id = message.from_user.id
    user_info = sqlite_bd.get_user_info(telegram_id)  # Предположим, что у вас есть функция для получения информации о пользователе из базы данных

    if user_info:
        date_reg, user_id, username, status = user_info
        response_text = f"Добро пожаловать в ваш личный кабинет!\n\n" \
                        f"Дата регистрации: {date_reg}\n" \
                        f"Ваш Telegram ID: {user_id}\n" \
                        f"Ваш юзернейм: @{username}\n"  \
                        f"Ваш Status ID: {status}"
    else:
        response_text = "Извините, не удалось получить информацию о вашем личном кабинете."

    # Отправляем ответ пользователю
    await message.from_user.id(response_text)
                         
@dp.message_handler()
async def handle_messages(message: types.Message):
    user = sqlite_bd.is_user_in_db(message.from_user.id)
    if user and user[0] == '0':
        await message.reply("Извините, у вас нет доступа к использованию бота.")
        return
    
async def on_shutdown(dp):
    await dp.bot.session.close()


