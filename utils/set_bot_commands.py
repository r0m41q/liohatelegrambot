from aiogram import types


async def set_default_commands(dp):
    await dp.bot.set_my_commands(
        [
            types.BotCommand("all", "To call upon the khuilyky"),
            types.BotCommand("pidor", "To choose one to rule them all"),
            types.BotCommand("fact", "It is what it is"),
            types.BotCommand("meme", "Facepalm"),
            types.BotCommand("stats", "Get stats"),
            types.BotCommand("help", "Get info"),
            types.BotCommand("statham", "To learn from the wisest of all men"),
        ]
    )
