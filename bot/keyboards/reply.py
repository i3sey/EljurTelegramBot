from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

chels = InlineKeyboardMarkup()

chels.add(InlineKeyboardButton('Классный руководитель', callback_data = 'classruks'))
chels.add(InlineKeyboardButton('Администрация', callback_data = 'administration'))
chels.add(InlineKeyboardButton('specialists', callback_data = 'specialists'))
chels.add(InlineKeyboardButton('teachers', callback_data = 'teachers'))
chels.add(InlineKeyboardButton('parents', callback_data = 'parents'))
chels.add(InlineKeyboardButton('students', callback_data = 'students'))
chels.add(InlineKeyboardButton('◀️', callback_data = 'backc'))
