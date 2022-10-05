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

set_receiver_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text='Хуйлики'),
            KeyboardButton(text='Тьом'),
            KeyboardButton(text='Льох'),
            KeyboardButton(text='Стьоп'),
            KeyboardButton(text='Ром'),
            KeyboardButton(text='Андрюх')
        ],
    ],
    resize_keyboard=True
)