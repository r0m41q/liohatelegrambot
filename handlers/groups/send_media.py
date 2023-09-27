import random
import time
from aiogram import types
from loader import dp, bot
from utils.db_api.mongodb import first_one_today, get_random_document, insert_use_of_function, get_memes, add_type_of_the_meme

okay_ids = [737410204,
            679885414,
            591400643,
            669554603,
            356854673]


@dp.message_handler(commands=['voice'])
async def say_pidor(message: types.Message):
    try:
        with open('./liohatelegrambot/data/voice/pidor.ogg', 'rb') as file:
            await bot.send_voice(message.chat.id, file)
    except FileNotFoundError:
        pass


@dp.message_handler(commands=['bomb'])
async def drop_bomb(message: types.Message):
    try:
        with open('./liohatelegrambot/data/voice/bomb.ogg', 'rb') as f:
            await bot.send_voice(message.chat.id, f)
    except FileNotFoundError:
        pass


@dp.message_handler(commands=['spam'])
async def send_all_memes(message: types.Message):
    memes_list = await get_memes('memes_id', 'meme_id')
    for meme_id in memes_list:
        await bot.send_photo(message.chat.id, meme_id)
        await message.answer(meme_id)
        time.sleep(8)


@dp.message_handler(commands=['meme'])
async def send_saved_photo(message: types.Message):
    if await first_one_today(message.chat.id, "meme"):
        meme = await get_random_document('memes_id', 'meme_id', type=True)  # get random meme_id

        if meme[1] == 'photo':
            meme_id = meme[0]
            await bot.send_photo(message.chat.id, meme_id)
            await message.answer(meme_id)
            await insert_use_of_function('meme', message.chat.id, message.from_user.username)  # write down use of function
        if meme[1] == 'video':
            meme_id = meme[0]
            await bot.send_video(message.chat.id, meme_id)
            await message.answer(meme_id)
            await insert_use_of_function('meme', message.chat.id, message.from_user.username)
        else:
            await message.answer('Шось пішло не так.')
    else:
        await bot.send_message(message.chat.id, "That much laugh can kill, you know")


@dp.message_handler(commands=['fact'])
async def send_fact(message: types.Message):
    user_id = message.from_user.id
    if user_id in okay_ids:
        if await first_one_today(message.chat.id, 'fact'):
            fact = await get_random_document('facts', 'fact')
            await message.answer(fact)
            await insert_use_of_function('fact', message.chat.id, message.from_user.username, fact=fact)

        else:
            await message.answer("You already got fact of the day, підор!")
    else:
        await insert_use_of_function('fact', message.chat.id, message.from_user.username)
        await message.answer("Fuck you, stranger")


@dp.message_handler(commands=['getsticker'])
async def send_random_sticker(message: types.Message):
    sticker_id = await get_random_document('stickers_id', 'sticker_id')
    await bot.send_sticker(message.chat.id, sticker_id)


@dp.message_handler(commands=['creator'])
async def show_creator(message: types.Message):
    await bot.send_sticker(message.chat.id, "CAADAgADlwADq5foJ7-Ri_InKepLFgQ")


@dp.message_handler(content_types=['sticker'])
async def send_random_sticker(message: types.Message):
    if random.randint(0, 9) == 1:
        sticker_id = await get_random_document('stickers_id', 'sticker_id')
        await bot.send_sticker(message.chat.id, sticker_id)


@dp.message_handler(content_types=['voice'])
async def say_something(message: types.Message):
    if random.randint(1, 55) == 2:
        await message.reply("Вот тобі понравиться, якшо я почну ноліками/одиничками общатись?")
