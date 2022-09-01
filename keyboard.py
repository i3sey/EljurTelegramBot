from aiogram import Bot, types
from aiogram.types import ReplyKeyboardRemove, ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton

######################################################
start = types.ReplyKeyboardMarkup(resize_keyboard=True) # СОЗДАЕМ ВООБЩЕ ОСНОВУ ДЛЯ КНОПОК

profile = types.KeyboardButton("хто я")            # ДОБАВЛЯЕМ КНОПКУ ИНФОРМАЦИИ
marks = types.KeyboardButton("предметы завтра")            # ДОБАВЛЯЕМ КНОПКУ СТАТИСТИКИ
peoples = types.KeyboardButton('Список челов')

#start.add(peoples)
start.add(marks, profile) #ДОБАВЛЯЕМ ИХ В БОТА


chels = InlineKeyboardMarkup()
chels.add(InlineKeyboardButton(f'Классный руководитель', callback_data = 'classruks'))
chels.add(InlineKeyboardButton(f'Администрация', callback_data = 'administration'))
chels.add(InlineKeyboardButton(f'specialists', callback_data = 'specialists'))
chels.add(InlineKeyboardButton(f'teachers', callback_data = 'teachers'))
chels.add(InlineKeyboardButton(f'parents', callback_data = 'parents'))
chels.add(InlineKeyboardButton(f'students', callback_data = 'students'))
chels.add(InlineKeyboardButton(f'◀️', callback_data = f'backc'))

