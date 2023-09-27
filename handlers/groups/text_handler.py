import re
import random
import time

from aiogram import types
from loader import dp, bot

from data.data_for_bot import pidora_otvet, vocab, say_it, khuilyky
from utils.db_api.mongodb import pidor_db, insert_new_meme, delete_the_meme
from utils.misc.time_functions import sent_recently
from utils.misc.eng_to_rus import replace_values_in_string


@dp.message_handler(commands=['all'])
async def call_everybody(message: types.Message):
    ping = re.sub(f'@{message.from_user.username}', '', khuilyky)
    await message.answer(ping)


@dp.message_handler(content_types=['text'])
async def say_pidor(message: types.Message):
    if f'players_{message.chat.id}' in await pidor_db.list_collection_names():
        pidor_collection = pidor_db[f'players_{message.chat.id}']
        today_pidor = await pidor_collection.find_one({"is_pidor": True})  # зчитуєм підора дня
        today_pidor = today_pidor['username']
        if sent_recently(message, 300):
            if message.from_user.username == f"{today_pidor}" and not message.forward_from:
                if random.randint(1, 12) == 1:  # 1/11 or 9% chance to trigger
                    await message.reply(random.choice(pidora_otvet))

    for key, value in vocab.items():
        if message.text.lower() == key.lower():
            await message.reply(value)

    for element in say_it:
        if message.text.lower() == element:
            with open('../../data/voice/pidor.ogg', 'rb') as f1:
                await bot.send_voice(message.chat.id, f1)
    try:
        if re.search(r'хуйлики', message.text.lower()).group(0) in message.text.lower():
            m1 = '<a href="tg://user?id=737410204">Хуй</a>'  # Артьом
            m2 = '<a href="tg://user?id=679885414">л</a>'    # Льоха
            m3 = '<a href="tg://user?id=591400643">и</a>'    # Стьопа
            m4 = '<a href="tg://user?id=669554603">к</a>'    # Андря_просто
            m5 = '<a href="tg://user?id=356854673">и</a>'    # Ромео

            await message.reply(m1 + m2 + m3 + m4 + m5, parse_mode=types.ParseMode.HTML)
    except AttributeError:
        pass

    if message.from_user.username == "Nonik000" and not message.forward_from:
        if 'андрюха, на завод' in message.text.lower():
            await bot.send_sticker(669554603, "CAACAgIAAxkBAAIQQGDJFyyPOG_lvycr1epvkxZWAAG8tAAC7gADq5foJ1usnmJLwGkOHwQ")
        if len(message.text) > 25:
            if random.randint(1, 30) == 1:
                await message.reply("Файно сказано")

    if message.text.lower() == 'в базу його':
        print(message)
        try:
            if message.reply_to_message.photo:
                file_id = message.reply_to_message.photo[2].file_id
                await insert_new_meme(file_id, 'photo')   # the path to file_id of the photo
                await message.reply("Your meme has been added!")

            if message.reply_to_message.video:
                file_id = message.reply_to_message.video.file_id
                await insert_new_meme(file_id, 'video')  # the path to file_id of the photo
                await message.reply("Your meme has been added!")

        except(IndexError, AttribureError):
            await message.reply("Something went wrong. The fault is probably yours, though.")

    if message.text.lower() == 'з бази його':
        try:
            if await delete_the_meme(message.reply_to_message.text):
                await message.reply("The meme has been deleted!")
            else:
                await message.reply("The meme is not in the db.")
        except AttributeError:
            await message.reply("Something went wrong. The fault is probably yours, though.")

    if message.text.lower() == 'вжух':
        try:
            changed_text = replace_values_in_string(message.reply_to_message.text)
            await message.reply(f'{changed_text}')
        except AttributeError:
            await message.reply("Хулі ти вжухаєш?")

    if message.text.lower() == 'жостко тебе марта, артьом?':
        try:
            with open('./liohatelegrambot/data/video/for_bot.mp4', 'rb') as f:
                await bot.send_video_note(message.chat.id, f)
        except FileNotFoundError:
            pass
