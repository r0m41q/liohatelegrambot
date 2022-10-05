from aiogram.dispatcher.filters.state import StatesGroup, State


class ForwardMsg(StatesGroup):
    get_receiver = State()
    get_msg = State()
    confirm_msg = State()
