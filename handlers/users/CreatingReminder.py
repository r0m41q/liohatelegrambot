import aioschedule

from aiogram import types
from loader import dp, bot
from aiogram.dispatcher import FSMContext, filters
from states.CreateReminder import CreateReminder
from keyboards.default import confirm_keyboard
from utils.db_api.mongodb import insert_reminder
from utils.misc.scheduler import scheduled_message


@dp.message_handler(commands=['cancel'], state='*')
async def cancel_state(message: types.Message, state: FSMContext):
    await state.finish()


@dp.message_handler(chat_type='private', commands=['create_reminder'])
async def forward_message(message: types.Message):
    await message.answer("What is the name of the reminder?")

    await CreateReminder.get_reminder_name.set()


@dp.message_handler(state=CreateReminder.get_reminder_name)
async def confirm_message(message: types.Message, state: FSMContext):

    await state.update_data(
        {"reminder_name": message.text}
    )

    await message.answer("What is the text of the reminder")

    await CreateReminder.get_reminder_text.set()


@dp.message_handler(state=CreateReminder.get_reminder_text)
async def confirm_message(message: types.Message, state: FSMContext):

    await state.update_data(
        {"reminder_text": message.text}
    )

    await message.answer("When do you want to be reminded?\nExample: 18:40")

    await CreateReminder.get_reminder_time.set()


@dp.message_handler(state=CreateReminder.get_reminder_time)
async def confirm_message(message: types.Message, state: FSMContext):
    #  we get time of reminding and should insert.
    await state.update_data(
        {"reminder_time": message.text}
    )

    await message.answer("Should this reminder repeat?\nWrite your interval or say 'no'")

    await CreateReminder.get_reminder_interval.set()


@dp.message_handler(state=CreateReminder.get_reminder_interval)
async def confirm_message(message: types.Message, state: FSMContext):
    #  we get interval or no interval
    if message.text.lower() == "no":
        await message.answer("The reminder has been created!")

        await state.finish()
    #  if is_proper_time():
    await state.update_data(
        {"reminder_interval": message.text}
    )
    data = await state.get_data()
    reminder_id = await insert_reminder(data, message.from_user.username, message.from_user.id)

    reminder_text = data['reminder_text']
    reminder_time = data['reminder_time']
    print(reminder_text)
    await message.answer("The reminder has been created!")
    aioschedule.every().day.at(f"{reminder_time}").do(scheduled_message, reminder_text, reminder_id)
    await state.finish()
