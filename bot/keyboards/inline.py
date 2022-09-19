from aiogram import types
start = types.ReplyKeyboardMarkup(resize_keyboard=True) # СОЗДАЕМ ВООБЩЕ ОСНОВУ ДЛЯ КНОПОК

profile = types.KeyboardButton("хто я")            # ДОБАВЛЯЕМ КНОПКУ ИНФОРМАЦИИ
marks = types.KeyboardButton("предметы завтра")            # ДОБАВЛЯЕМ КНОПКУ СТАТИСТИКИ
peoples = types.KeyboardButton('Список челов')
start.add(marks, profile)