from aiogram import types

buttons = [
        [
            types.InlineKeyboardButton(text="Не", callback_data="nope"),
            types.InlineKeyboardButton(text="Дай я", callback_data="edit"),
            types.InlineKeyboardButton(text="Норм", callback_data="ok")
    ]]
keyboard = types.InlineKeyboardMarkup(inline_keyboard=buttons)