import ast
import random
import re

from aiogram import types
from loader import dp


@dp.message_handler(commands=['statham'])
async def send_quote(message: types.Message):
    clean_quotes = []
    with open('data/quotes/statham_quotes.txt', 'r', encoding='utf-8') as file:
        quotes = file.readlines()
    for quote in quotes:
        quote = ast.literal_eval(quote)
        clean_quotes.append(quote)
    await message.answer(random.choice(clean_quotes))


@dp.message_handler(commands=['quote'])
async def send_quote(message: types.Message):
    clean_quotes = []
    with open('data/quotes/qt_clean.txt', 'r', encoding='utf-8') as file:
        quotes = file.readlines()
    for quote in quotes:
        quote = re.sub(' \u00A9 ', '\n\u00A9 ', quote)
        clean_quotes.append(quote)
    await message.answer(random.choice(clean_quotes))
