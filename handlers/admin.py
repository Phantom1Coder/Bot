from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram import types
from create_bot import dp



class FSMAdmin(StatesGroup):
    text = State()
    description = State()


@dp.message_handler(lambda message: message.text.lower() == '/cancel', state=FSMAdmin)
async def cancel_handler(message: types.Message, state: FSMContext):
    current_state = await state.get_state()
    if current_state is None:
        return
    
    await state.finish()
    await message.reply("Выход из режима изменения.")

@dp.message_handler(commands=('Изменить'), state=None)
async def cm_start(message: types.Message):
    await FSMAdmin.text.set()
    await message.reply('Введите новое название кнопки')

@dp.message_handler(state=FSMAdmin.text)
async def new_dcp(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['text'] = message.text
    await FSMAdmin.description.set()
    await message.reply("Введи новое описание")

@dp.message_handler(state=FSMAdmin.description)
async def new_description(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['description'] = message.text 
         
    await state.finish()
    await message.reply("Изменения сохранены")
