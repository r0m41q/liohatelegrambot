import random

from aiogram import types
from loader import dp
from utils.db_api.mongodb import pidor_db, insert_use_of_function, first_one_today
from handlers.groups.send_media import send_saved_photo, send_fact


@dp.message_handler(commands=['startgame'])
async def get_players_usernames(message: types.Message):
    username = message.from_user.username
    pidor_collection = pidor_db[f'players_{message.chat.id}']

    if await pidor_collection.find_one({"user_id": message.from_user.id}):

        await message.reply("You are already in the game!")
    else:
        new_player = {"username": f"{username}",
                      "user_id": message.from_user.id,
                      "score": 0,
                      "is_pidor": False,
                      }
        await pidor_collection.insert_one(new_player)
        await message.reply("Congrats, you are in the game!")


@dp.message_handler(commands=['pidor'])
async def pidor_dnya(message: types.Message):
    if f'players_{message.chat.id}' in await pidor_db.list_collection_names():
        if await first_one_today(message.chat.id, 'pidor'):
            pidor_collection = pidor_db[f'players_{message.chat.id}']             # колекція списку гравців
            pidor_list = pidor_collection.find()
            players_usernames = []
            async for pidor in pidor_list:  # додаєм нікнейми в список
                players_usernames.append(pidor['username'])

            await pidor_collection.update_many({}, {"$set": {"is_pidor": False}})  # обнуляєм всім статус підара

            today_pidor = random.choice(players_usernames)

            filter_ = {'username': f'{today_pidor}'}
            new_values = {"$inc": {'score': 1},
                          "$set": {"is_pidor": True}
                          }
            await pidor_collection.update_one(filter_, new_values)  # збільшуєм рахунок на 1, і задаєм статус підара

            await insert_use_of_function('pidor', message.chat.id, message.from_user.username)

            await message.answer(f"@{today_pidor} you are pidar!")
        else:
            pidor_collection = pidor_db[f'players_{message.chat.id}']
            today_pidor = await pidor_collection.find_one({"is_pidor": True})
            today_pidor = today_pidor['username']  # зчитуєм підора дня
            await message.answer(f"Підар дня:\n{today_pidor}")
    else:
        await message.answer("Use /startgame first.")


@dp.message_handler(commands=['me'])
async def how_many_times(message: types.Message):
    if f'players_{message.chat.id}' in await pidor_db.list_collection_names():  # якшо є запис для цього чату
        pidor_collection = pidor_db[f'players_{message.chat.id}']         # список підарів
        if await pidor_collection.find_one({"user_id": message.from_user.id}):  # якшо є підар, який викликав команду
            score = await pidor_collection.find_one({"user_id": message.from_user.id})
            score = score['score']  # рахунок цього підара
            await message.answer(f"You are {score} times pidor")
        else:
            await message.answer("You should be part of the game to see your stats")
    else:
        await message.answer("You should be part of the game to see stats")


@dp.message_handler(commands=['stats'])
async def statistics(message: types.Message):
    if f'players_{message.chat.id}' in await pidor_db.list_collection_names():
        stats = []
        pidor_collection = pidor_db[f'players_{message.chat.id}']
        pidor_list = pidor_collection.find({})                         # список підарів в descending порядку
        async for pidor in pidor_list.sort('score', -1):
            stats.append(f"{pidor['username']} - {pidor['score']}\n")  # оформлюємо інфу з бд у вигляді Nonik000 - 8

        await message.answer(''.join(stats))  # зі списка робим стрічку

    else:
        await message.answer("Nobody in your chat is playing.")


@dp.message_handler(commands=['bundle'])
async def bundle(message: types.Message):
    await pidor_dnya(message)
    await send_fact(message)
    await send_saved_photo(message)
