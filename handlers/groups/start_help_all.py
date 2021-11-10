from aiogram import types
from loader import dp
from aiogram.dispatcher.filters.builtin import CommandHelp, CommandStart
from data.data_for_bot import Help, Hello


@dp.message_handler(commands=['helppp'])
async def bot_help(message: types.Message):
    await message.answer(Help)


@dp.message_handler(commands=['start'])
async def bot_start(message: types.Message):
    print("fgwgeg")
    await message.answer("іацупацупц")



