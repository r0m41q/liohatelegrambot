from aiogram.dispatcher.filters.state import StatesGroup, State


class ForwardPhoto(StatesGroup):
    get_photo = State()
    confirm_photo = State()
