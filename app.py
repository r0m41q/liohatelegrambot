from aiogram import executor

from loader import dp
import middlewares, filters, handlers

import asyncio
from threading import Thread

from utils.notify_admins import on_startup_notify
from utils.set_bot_commands import set_default_commands
from utils.misc.scheduler import scheduler
from utils.db_api.mongodb import get_reminders


async def on_startup(dispatcher):
    # Устанавливаем дефолтные команды
    await set_default_commands(dispatcher)

    # Уведомляет про запуск
    await on_startup_notify(dispatcher)

    asyncio.create_task(scheduler())
    Thread(target=scheduler).start()

    # get_reminders(679885414)

if __name__ == '__main__':
    executor.start_polling(dp, on_startup=on_startup, skip_updates=True)
