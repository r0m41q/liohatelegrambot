from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

confirm_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text='Yes'),
            KeyboardButton(text='No')
        ],
    ],
    resize_keyboard=True
)