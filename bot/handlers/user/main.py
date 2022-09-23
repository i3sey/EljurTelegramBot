import datetime
from email import message
from email.message import Message

from aiogram import Dispatcher
from aiogram.dispatcher.filters import Command
from aiogram.dispatcher.filters.state import State, StatesGroup
from bot.database.main import DiaryDB
from bot.keyboards import inline
from bot.misc.util import lessones
from bot.misc.util import info


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
        
async def lessons(msg: Message):
    r = await msg.answer('<b>Секунду...</b>')
    await r.edit_text(text=await lessones(msg))

async def information(msg: Message):
    r = await msg.answer('<b>Секунду...</b>')
    await r.edit_text(text=await info(msg))
    
def register_user_handlers(dp: Dispatcher):
    # todo: register all user handlers
    dp.register_message_handler(update, Command("update"), state=None)
    dp.register_message_handler(start, Command("start"), state=None)
    dp.register_message_handler(lessons, lambda message: message.text == "предметы завтра", state=None)
    dp.register_message_handler(information, lambda message: message.text == "хто я", state=None)
    

