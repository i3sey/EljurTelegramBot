from aiogram import types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

######################################################
start = types.ReplyKeyboardMarkup(resize_keyboard=True) # СОЗДАЕМ ВООБЩЕ ОСНОВУ ДЛЯ КНОПОК

profile = types.KeyboardButton("хто я")            # ДОБАВЛЯЕМ КНОПКУ ИНФОРМАЦИИ
marks = types.KeyboardButton("предметы завтра")            # ДОБАВЛЯЕМ КНОПКУ СТАТИСТИКИ
peoples = types.KeyboardButton('Список челов')

#start.add(peoples)
start.add(marks, profile) #ДОБАВЛЯЕМ ИХ В БОТА


chels = InlineKeyboardMarkup()
chels.add(InlineKeyboardButton('Классный руководитель', callback_data = 'classruks'))
chels.add(InlineKeyboardButton('Администрация', callback_data = 'administration'))
chels.add(InlineKeyboardButton('specialists', callback_data = 'specialists'))
chels.add(InlineKeyboardButton('teachers', callback_data = 'teachers'))
chels.add(InlineKeyboardButton('parents', callback_data = 'parents'))
chels.add(InlineKeyboardButton('students', callback_data = 'students'))
chels.add(InlineKeyboardButton('◀️', callback_data = 'backc'))
