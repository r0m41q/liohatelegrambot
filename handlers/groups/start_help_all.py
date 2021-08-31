import re

from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandHelp, CommandStart
from loader import dp

from data.data_for_bot import Help, Hello


@dp.message_handler(commands=['help'])
async def bot_help(message: types.Message):
    await message.answer(Help)


@dp.message_handler(commands=['start'])
async def bot_start(message: types.Message):
    await message.answer(Hello)



