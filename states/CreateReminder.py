from aiogram.dispatcher.filters.state import StatesGroup, State


class CreateReminder(StatesGroup):
    get_reminder_name = State()
    get_reminder_text = State()
    get_reminder_time = State()
    get_reminder_interval = State()
