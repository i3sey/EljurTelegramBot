from aiogram import types
kb = [
      # [types.KeyboardButton(text="распознать домашку завтра")],
      [types.KeyboardButton(text="домашка завтра")],
      [types.KeyboardButton(text="хто я"), types.KeyboardButton(text="предметы завтра")]]
start = types.ReplyKeyboardMarkup(
        keyboard=kb,
        resize_keyboard=True,
        input_field_placeholder="Выберите Действие: "
    )