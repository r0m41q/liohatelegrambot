import time
import language_tool_python

from aiogram import types
from loader import bot

tool = language_tool_python.LanguageTool('uk')

async def correct_your_ass(message: types.Message):
    if len(message.text) > 8:
        is_bad_rule = lambda rule: rule.message == 'Це речення не починається з великої літери.' \
                                   and len(rule.replacements) and rule.replacements[0][0].isupper()
        matches = tool.check(message.text)
        matches = [rule for rule in matches if not is_bad_rule(rule)]

        if len(matches) > 1:
            forward_to_lexa = language_tool_python.utils.correct(message.text, matches)
            await bot.send_message(679885414, f"Original messsage:\n{message.text}\n"
                                              f"Here is possible correction:\n{forward_to_lexa}")

        if len(matches) > 2:
            proposal = language_tool_python.utils.correct(message.text, matches)
            time.sleep(2)
            await bot.send_sticker(message.chat.id,
                                   "CAACAgIAAxkBAAIQGmDJFtMDPbe4OIHIrCyyHCJjFK9jAALvAAOrl-gnY1y2wnXZiEUfBA")
            await bot.send_chat_action(message.chat.id, 'typing')
            time.sleep(5)
            await message.reply(f'{proposal}')