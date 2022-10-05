from aiogram import types
from loader import dp, bot
from aiogram.dispatcher import FSMContext, filters
from states.ForwardMessage import ForwardMsg
from keyboards.default import confirm_keyboard, set_receiver_keyboard

id_list = {"Хуйлики": -1001457164397, "Тьом": 737410204, "Льох": 679885414,
       "Стьоп": 591400643, "Андрюх": 669554603, "Ром": 356854673}


@dp.message_handler(commands=['cancel'], state='*')
async def cancel_state(message: types.Message, state: FSMContext):
    await state.finish()


@dp.message_handler(chat_type='private', commands=['anon_msg'])
async def forward_message(message: types.Message):
    await message.answer("Кому адресується ваше чудове послання?", reply_markup=set_receiver_keyboard)

    await ForwardMsg.get_receiver.set()


@dp.message_handler(state=ForwardMsg.get_receiver)
async def forward_message(message: types.Message, state: FSMContext):

    for key, value in id_list.items():
        if message.text.lower() == key.lower():
            receiver_id = value

    await state.update_data(
        {"receiver_id": receiver_id}
    )

    await message.answer(f"What would you like to send?", reply_markup=types.ReplyKeyboardRemove())

    await ForwardMsg.get_msg.set()


@dp.message_handler(state=ForwardMsg.get_msg)
async def confirm_message(message: types.Message, state: FSMContext):
    user_message = message.text

    await state.update_data(
        {"user_message": user_message}
    )

    await message.answer(f"Are you sure this is the message you want to send?:\n\n{user_message}",
                         reply_markup=confirm_keyboard)

    await ForwardMsg.confirm_msg.set()


@dp.message_handler(state=ForwardMsg.confirm_msg)
async def confirm_message(message: types.Message, state: FSMContext):
    data = await state.get_data()
    user_message = data.get("user_message")
    receiver_id = data.get("receiver_id")
    answer = message.text
    print(answer)
    if answer.lower() == 'yes':
        await bot.send_message(receiver_id, f'{user_message}')
        await message.answer("Done!", reply_markup=types.ReplyKeyboardRemove())
    else:
        await message.answer("No message will be sent.", reply_markup=types.ReplyKeyboardRemove())
    await state.finish()
