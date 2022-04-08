from aiogram import types

from loader import dp, bot
from utils.db_api.mongodb import insert_logs_to_db, delete_all_logs


@dp.message_handler(commands=['reminder'])
async def reminder_message(message: types.Message):
    await bot.send_message()


@dp.message_handler(commands=['log'])
async def display_log(message: types.Message):
    await insert_logs_to_db()
    await message.answer("The log is displayed")


@dp.message_handler(commands=['clear'])
async def reminder_message(message: types.Message):
    with open("app.log", 'w') as file:
        file.write("executor.py [LINE:362] #INFO [2022-03-22 16:41:54,012] "
                   "[MainThread  ]  Bot: Tyomatest [@Tyomatest_bot]")
    await message.answer("The log is cleared!")


@dp.message_handler(commands=['delete_logs'])
async def delete_logs(message: types.Message):
    await delete_all_logs()
    await message.answer("The logs are deleted from DB!")