from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove, InlineKeyboardButton, InlineKeyboardMarkup

k1 = KeyboardButton('/Menu')
k2 = KeyboardButton('/Перевод')
k3 = KeyboardButton('/help')

kb_client = ReplyKeyboardMarkup(resize_keyboard=True)

kb_client.add(k1).add(k2).add(k3)

language = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
buttons = [
    KeyboardButton("Английский"),
    KeyboardButton("Русский"),
    KeyboardButton("Французский"),
    # Добавьте кнопки для других языков
]
language.add(*buttons)