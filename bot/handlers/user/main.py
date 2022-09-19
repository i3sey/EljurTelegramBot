from email.message import Message

from aiogram import Dispatcher
from aiogram.dispatcher.filters import Command
from aiogram.dispatcher.filters.state import State, StatesGroup
from bot.database.main import DiaryDB
from bot.keyboards import inline


class UserInfo(StatesGroup):
    QL = State()
    QP = State()
    QD = State()
    
async def update(msg: Message):
    DiaryDB('database.db').resetdb()
    await msg.answer("Кнопки были успешно обновлены!", reply_markup=inline.start)

async def start(msg: Message):
    PeopleId = DiaryDB('database.db').get(f'{msg.chat.id}_login')
    if PeopleId == False:
        await msg.answer('Привет, гони логин')
        await UserInfo.QL.set()
    else:
        await msg.answer("Кнопки были успешно обновлены!", reply_markup=inline.start)
        
def register_user_handlers(dp: Dispatcher):
    # todo: register all user handlers
    dp.register_message_handler(update, Command("update"), state=None)
    dp.register_message_handler(start, Command("start"), state=None)

