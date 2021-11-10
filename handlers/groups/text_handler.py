import re
import random
import time
import language_tool_python

from aiogram import types
from loader import dp, bot

from data.data_for_bot import pidora_otvet, vocab, say_it, khuilyky
from utils.db_api.mongodb import pidor_db
from utils.misc.time_functions import sent_recently
from utils.misc.eng_to_rus import replace_values_in_string
tool = language_tool_python.LanguageToolPublicAPI('uk')


@dp.message_handler(commands=['all'])
async def call_everybody(message: types.Message):
    ping = re.sub(f'@{message.from_user.username}', '', khuilyky)
    await message.answer(ping)


@dp.message_handler(content_types=['text'])
async def say_pidor(message: types.Message):
    if f'players_{message.chat.id}' in pidor_db.list_collection_names():
        pidor_collection = pidor_db[f'players_{message.chat.id}']
        today_pidor = pidor_collection.find_one({"is_pidor": True})['username']  # зчитуєм підора дня

        if sent_recently(message, 300):
            if message.from_user.username == f"{today_pidor}" and not message.forward_from:
                if random.randint(1, 12) == 1:  # 1/11 or 9% chance to trigger
                    await message.reply(random.choice(pidora_otvet))

    for key, value in vocab.items():
        if message.text.lower() == key.lower():
            await message.reply(value)

    for element in say_it:
        if message.text.lower() == element:
            with open('data/voice/pidor.ogg', 'rb') as f1:
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
            await bot.send_sticker(679885414, "CAACAgIAAxkBAAIQQGDJFyyPOG_lvycr1epvkxZWAAG8tAAC7gADq5foJ1usnmJLwGkOHwQ")
        if len(message.text) > 25:
            if random.randint(1, 30) == 1:
                await message.reply("Как боженька молвил")

    if message.from_user.username == "prosto_andrya":
        if len(message.text) > 8:
            is_bad_rule = lambda rule: rule.message == 'Це речення не починається з великої літери.' \
                                       and len(rule.replacements) and rule.replacements[0][0].isupper()
            matches = tool.check(message.text)
            matches = [rule for rule in matches if not is_bad_rule(rule)]

            if len(matches) > 1:
                forward_to_lexa = language_tool_python.utils.correct(message.text, matches)
                await bot.send_message(679885414, f"Original messsage:\n{message.text}\n"
                                                  f"Here is possible correction:\n{forward_to_lexa}")

            if len(matches) > 2:
                proposal = language_tool_python.utils.correct(message.text, matches)
                time.sleep(2)
                await bot.send_sticker(message.chat.id,
                                       "CAACAgIAAxkBAAIQGmDJFtMDPbe4OIHIrCyyHCJjFK9jAALvAAOrl-gnY1y2wnXZiEUfBA")
                await bot.send_chat_action(message.chat.id, 'typing')
                time.sleep(5)
                await message.reply(f'{proposal}')

    if message.text.lower() == 'вжух':
        try:
            changed_text = replace_values_in_string(message.reply_to_message.text)
            await message.reply(f'{changed_text}')
        except AttributeError:
            await message.reply("Хулі ти вжухаєш?")

    if message.text.lower() == 'жостко тебе марта, артьом?':
        try:
            with open('data/video/for_bot.mp4', 'rb') as f:
                await bot.send_video_note(message.chat.id, f)
        except FileNotFoundError:
            pass
