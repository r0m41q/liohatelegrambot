from aiogram import types
from loader import dp, bot
from aiogram.dispatcher import FSMContext, filters
from states.ForwardPhoto import ForwardPhoto
from keyboards.default import confirm_keyboard


@dp.message_handler(commands=['cancel'], state='*')
async def cancel_state(message: types.Message, state: FSMContext):
    await state.finish()


@dp.message_handler(chat_type='private', commands=['anon_photo'])
async def forward_message(message: types.Message):
    await message.answer("What would you like to send to khuilyky?")

    await ForwardPhoto.get_photo.set()


@dp.message_handler(content_types=['photo'], state=ForwardPhoto.get_photo)
async def confirm_message(message: types.Message, state: FSMContext):
    user_message = message.photo[0].file_id
    print(user_message)
    await state.update_data(
        {"user_photo": user_message}
    )

    await message.answer(f"Are you sure this is the message you want to send?:\n\n{user_message}",
                         reply_markup=confirm_keyboard)

    await ForwardPhoto.confirm_photo.set()


@dp.message_handler(state=ForwardPhoto.confirm_photo)
async def confirm_message(message: types.Message, state: FSMContext):
    data = await state.get_data()
    user_photo = data.get("user_photo")
    answer = message.text
    print(answer)
    if answer.lower() == 'yes':
        await bot.send_photo(679885414, user_photo)
        await message.answer("Done!", reply_markup=types.ReplyKeyboardRemove())
    else:
        await message.answer("No message will be sent.", reply_markup=types.ReplyKeyboardRemove())
    await state.finish()
