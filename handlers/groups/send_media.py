import random
from aiogram import types
from loader import dp, bot
from utils.db_api.mongodb import first_one_today, get_random_document, insert_use_of_function


@dp.message_handler(commands=['voice'])
async def say_pidor(message: types.Message):
    try:
        with open('data/voice/pidor.ogg', 'rb') as file:
            await bot.send_voice(message.chat.id, file)
    except FileNotFoundError:
        pass


@dp.message_handler(commands=['bomb'])
async def drop_bomb(message: types.Message):
    try:
        with open('data/voice/bomb.ogg', 'rb') as f:
            await bot.send_voice(message.chat.id, f)
    except FileNotFoundError:
        pass


@dp.message_handler(commands=['meme'])
async def send_saved_photo(message: types.Message):
    if first_one_today(message.chat.id, "meme"):
        meme_id = get_random_document('memes_id', 'meme_id')  # get random meme_id
        await bot.send_photo(message.chat.id, meme_id)
        insert_use_of_function('meme', message.chat.id)       # write down use of function
    else:
        await bot.send_message(message.chat.id, "That much laugh can kill, you know")


@dp.message_handler(commands=['fact'])
async def send_fact(message: types.Message):
    if first_one_today(message.chat.id, 'fact'):
        fact = get_random_document('facts', 'fact')
        await message.answer(fact)
        insert_use_of_function('fact', message.chat.id)

    else:
        await message.answer("You already got fact of the day, підор!")


@dp.message_handler(commands=['getsticker'])
async def send_random_sticker(message: types.Message):
    sticker_id = get_random_document('stickers_id', 'sticker_id')
    await bot.send_sticker(message.chat.id, sticker_id)


@dp.message_handler(commands=['creator'])
async def show_creator(message: types.Message):
    await bot.send_sticker(message.chat.id, "CAADAgADlwADq5foJ7-Ri_InKepLFgQ")


@dp.message_handler(content_types=['sticker'])
async def send_random_sticker(message: types.Message):
    if random.randint(0, 9) == 1:
        sticker_id = get_random_document('stickers_id', 'sticker_id')
        await bot.send_sticker(message.chat.id, sticker_id)


@dp.message_handler(content_types=['voice'])
async def say_something(message: types.Message):
    if random.randint(1, 55) == 2:
        await message.reply("Вот тобі понравиться, якшо я почну ноліками/одиничками общатись?")
