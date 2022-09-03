import datetime
import logging
import os
from sys import platform

from aiogram import Bot, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import Dispatcher, FSMContext
from aiogram.dispatcher.filters import Command
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils import executor

import api
import keyboard

if platform == 'win32':
    from config import TESTTOKEN
    BOTKEY = TESTTOKEN
else:
    BOTKEY = os.environ['STDTOKEN']

storage = MemoryStorage()  # FOR FSM
bot = Bot(token=BOTKEY, parse_mode=types.ParseMode.HTML)
dp = Dispatcher(bot, storage=storage)
logging.basicConfig(
    format='%(filename)s [LINE:%(lineno)d] #%(levelname)-8s [%(asctime)s]  %(message)s'
    , level=logging.INFO,)


class UserInfo(StatesGroup):
    QL = State()
    QP = State()
    QD = State()


def cleanup(dictionary):
    result = '\n'.join(
        [f'{key.capitalize()}: {value}' for key, value in dictionary.items()])
    return result


@dp.message_handler(Command("update"), state=None)
async def update(message: types.Message):
    await bot.send_message(message.chat.id, "Кнопки были успешно обновлены!",
                           reply_markup=keyboard.start,
                           parse_mode='Markdown')


@dp.message_handler(Command("start"), state=None)
async def start(message: types.Message):
    joined_file = open("user.txt", "r", encoding='utf-8')
    joined_users = set()
    for line in joined_file:
        joined_users.add(line.strip())

    if not str(message.chat.id) in joined_users:
        joined_file = open("user.txt", "a", encoding='utf-8')
        joined_file.write(str(message.chat.id) + "\n")
        joined_users.add(message.chat.id)
    await message.answer('Привет, гони логин')
    await UserInfo.QL.set()


@dp.message_handler(state=UserInfo.QL)
async def login(message: types.Message, state: FSMContext):
    user_login = message.text
    await state.update_data(answer1=user_login)
    await message.answer('пароль дай')
    await UserInfo.QP.set()


@dp.message_handler(state=UserInfo.QP)
async def password(message: types.Message, state: FSMContext):
    user_password = message.text
    await state.update_data(answer2=user_password)
    await message.answer('домен дай')
    await UserInfo.QD.set()


@dp.message_handler(state=UserInfo.QD)
async def domain(message: types.Message, state: FSMContext):
    user_domain = message.text
    await state.update_data(answer3=user_domain)
    await message.answer('сек, чекаю')
    await UserInfo.QD.set()

    data = await state.get_data()
    user_login = data.get("answer1")
    user_password = data.get("answer2")
    user_domain = data.get("answer3")

    getter = api.newUser(message.chat.id, str(user_login),
                         str(user_password), str(user_domain))
    if getter != 0:
        await message.answer('Произошла ошибка, убедитесь в праильности введённых данных')
        # Есть идея ещё код ошибки докинуть  TODO
        await message.answer('Привет, гони логин')
        await UserInfo.QL.set()
    else:
        await bot.send_message(message.chat.id,
                               f"ПРИВЕТ, *{api.idProfile(message.chat.id)['Имя']},* БОТ РАБОТАЕТ",
                               reply_markup=keyboard.start,
                               parse_mode='Markdown')
        await state.finish()


@dp.message_handler(content_types=['text'])
async def get_message(message):
    match message.text:
        case "хто я":
            sec = await bot.send_message(message.chat.id, '**Секунду...**', parse_mode='Markdown')
            dictionary = api.idProfile(message.chat.id)
            result = cleanup(dictionary)
            await bot.edit_message_text(text=result,
                                        chat_id=message.chat.id,
                                        message_id=sec.message_id,
                                        parse_mode='Markdown')
        case 'предметы завтра':
            time_zone = datetime.timezone(datetime.timedelta(hours=5))
            sec = await bot.send_message(message.chat.id, '**Секунду...**', parse_mode='Markdown')
            date = datetime.datetime.now(time_zone) + datetime.timedelta(days=1)
            if date.weekday() == 5:
                date += datetime.timedelta(days=2)
            elif date.weekday() == 6:
                date += datetime.timedelta(days=1)
            today_week = datetime.datetime.now(time_zone).weekday()
            if today_week == 6 or today_week == 5:
                dictionary = api.idJournal(message.chat.id, 1)
            else:
                dictionary = api.idJournal(message.chat.id, 0)
            day = date.strftime("%d")
            date_str = date.strftime(f"{day}.%m")
            for key, val in dictionary.items():
                if val['date'] == date_str:
                    tommorow_day = key
            if dictionary[tommorow_day]['isEmpty'] is True:
                lessones = 'Уроков нет, отдыхаем'
            else:
                lessones = cleanup(dictionary[tommorow_day]['lessons'])
            render = f'Завтра *{tommorow_day}, {date_str}*\n{lessones}'
            await bot.edit_message_text(text=render,
                                        chat_id=message.chat.id,
                                        message_id=sec.message_id,
                                        parse_mode='Markdown')
        case 'Список челов':
            await bot.send_message(message.chat.id,
                                   text="Выберете категорию",
                                   reply_markup=keyboard.chels,
                                   parse_mode='Markdown')


@dp.callback_query_handler(text_contains='classruks')
async def classruks(call: types.CallbackQuery):
    dictionary_peoples = api.peopleList('classruks')
    chelsa = InlineKeyboardMarkup()
    for key, val in dictionary_peoples.items():
        chelsa.add(InlineKeyboardButton(f'{key}', callback_data=f'{val}'))
    chelsa.add(InlineKeyboardButton('◀️', callback_data='back'))
    await bot.edit_message_text(chat_id=call.message.chat.id,
                                message_id=call.message.message_id,
                                text='Выбери:',
                                reply_markup=chelsa)
    await bot.answer_callback_query(callback_query_id=call.id)


@dp.callback_query_handler(text_contains='administration')
async def administration(call: types.CallbackQuery):
    dictionary_peoples = api.peopleList('administration')
    chelsa = InlineKeyboardMarkup()
    for key, val in dictionary_peoples.items():
        chelsa.add(InlineKeyboardButton(f'{key}', callback_data=f'{val}'))
    chelsa.add(InlineKeyboardButton('◀️', callback_data='back'))
    await bot.edit_message_text(chat_id=call.message.chat.id,
                                message_id=call.message.message_id,
                                text='Выбери:',
                                reply_markup=chelsa)
    await bot.answer_callback_query(callback_query_id=call.id)


@dp.callback_query_handler(text_contains='specialists')
async def specialists(call: types.CallbackQuery):
    dictionary_peoples = api.peopleList('specialists')
    chelsa = InlineKeyboardMarkup()
    for key, val in dictionary_peoples.items():
        chelsa.add(InlineKeyboardButton(f'{key}', callback_data=f'{val}'))
    chelsa.add(InlineKeyboardButton('◀️', callback_data='back'))
    await bot.edit_message_text(chat_id=call.message.chat.id,
                                message_id=call.message.message_id,
                                text='Выбери:',
                                reply_markup=chelsa)
    await bot.answer_callback_query(callback_query_id=call.id)


@dp.callback_query_handler(text_contains='teachers')
async def teachers(call: types.CallbackQuery):
    dictionary_peoples = api.peopleList('teachers')
    chelsa = InlineKeyboardMarkup()
    for key, val in dictionary_peoples.items():
        chelsa.add(InlineKeyboardButton(f'{key}', callback_data=f'{val}'))
    chelsa.add(InlineKeyboardButton('◀️', callback_data='back'))
    await bot.edit_message_text(chat_id=call.message.chat.id,
                                message_id=call.message.message_id,
                                text='Выбери:',
                                reply_markup=chelsa)
    await bot.answer_callback_query(callback_query_id=call.id)


@dp.callback_query_handler(text_contains='parents')
async def parents(call: types.CallbackQuery):
    dictionary_peoples = api.peopleList('parents')
    chelsa = InlineKeyboardMarkup()
    for key, val in dictionary_peoples.items():
        chelsa.add(InlineKeyboardButton(f'{key}', callback_data=f'{val}'))
    chelsa.add(InlineKeyboardButton('◀️', callback_data='back'))
    await bot.edit_message_text(chat_id=call.message.chat.id,
                                message_id=call.message.message_id,
                                text='Выбери:',
                                reply_markup=chelsa)
    await bot.answer_callback_query(callback_query_id=call.id)


@dp.callback_query_handler(text_contains='students')
async def students(call: types.CallbackQuery):
    dictionary_peoples = api.peopleList('students')
    chelsa = InlineKeyboardMarkup()
    for key, val in dictionary_peoples.items():
        chelsa.add(InlineKeyboardButton(f'{key}', callback_data=f'{val}'))
    chelsa.add(InlineKeyboardButton('◀️', callback_data='back'))
    await bot.edit_message_text(chat_id=call.message.chat.id,
                                message_id=call.message.message_id,
                                text='Выбери:',
                                reply_markup=chelsa)
    await bot.answer_callback_query(callback_query_id=call.id)


@dp.callback_query_handler(text_contains='backc')
async def backc(call: types.CallbackQuery):
    for i in range(2):
        await bot.delete_message(call.message.chat.id, call.message.message_id-i)


@dp.callback_query_handler(text_contains='back')
async def back(call: types.CallbackQuery):
    await call.message.edit_text(text="Выберете категорию",
                                 reply_markup=keyboard.chels,
                                 parse_mode='Markdown')


if __name__ == '__main__':
    print('Монстр пчелы запущен!')
executor.start_polling(dp)
