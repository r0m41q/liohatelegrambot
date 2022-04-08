import aioschedule
import asyncio

from threading import Thread

from aiogram import types

from loader import dp, bot
from utils.db_api.mongodb import get_reminders, log_reminder, insert_logs_to_db


async def scheduled_message(reminder_text, reminder_id):
    await bot.send_message(679885414, f"{reminder_text}")
    await log_reminder(679885414, reminder_id)


async def scheduler():
    # reminder_text, reminder_time, reminder_id = get_reminders(679885414)
    list_of_reminders = await get_reminders(679885414)
    # print(list_of_reminders)
    for reminder in list_of_reminders:
        reminder_text = reminder["reminder_text"]
        reminder_time = reminder["reminder_time"]
        reminder_id = reminder["_id"]
        # print(reminder_text, reminder_time, reminder_id)
        # print("END OF REMINDER\n")
        aioschedule.every().day.at(f"{reminder_time}").do(scheduled_message, reminder_text, reminder_id)
    aioschedule.every(5).hours.do(insert_logs_to_db)
    # Thread(target=scheduler).start()
    while True:
        await aioschedule.run_pending()
        await asyncio.sleep(10)

