from email.message import Message

from aiogram import Router, types
from aiogram.filters.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from bot.database import main
from bot.keyboards import reply
from bot.misc.util import info, lessones, Homeworks
from aiogram import F

class UserInfo(StatesGroup):
    QL = State()
    QP = State()
    QD = State()
    
router = Router()

@router.message(commands=["reset"])
async def update(msg: Message):
    main.DiaryDB('database.db').resetdb()
    await msg.answer("Кнопки были успешно обновлены!", reply_markup=reply.start)
    
@router.message(commands=["start"])
async def start(msg: types.Message, state: FSMContext):
    PeopleId = main.DiaryDB('database.db').get(f'{msg.chat.id}_login')
    if PeopleId == False:
        await msg.answer('Привет, гони логин')
        await state.set_state(UserInfo.QL)
    else:
        await msg.answer("Кнопки были успешно обновлены!", reply_markup=reply.start)

@router.message(F.text == "домашка завтра")
async def homework(msg: Message):
    r = await msg.answer('<b>Секунду...</b>')
    await r.edit_text(text=await Homeworks(msg))
        
@router.message(F.text == "предметы завтра")
async def lessons(msg: Message):
    r = await msg.answer('<b>Секунду...</b>')
    await r.edit_text(text=await lessones(msg))
    
@router.message(F.text == "хто я")
async def information(msg: Message):
    r = await msg.answer('<b>Секунду...</b>')
    await r.edit_text(text=await info(msg))
    