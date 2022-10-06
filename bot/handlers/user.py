from email.message import Message

from aiogram import Router, types
from aiogram.filters.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from bot.database import main
from bot.keyboards import reply
from bot.functions import info, lessonsToday, recognize, tommorow, tommorowHw, gdzAsking
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
    await r.edit_text(text=await tommorowHw.Homeworks(msg))


@router.message(F.text == "предметы завтра")
async def lessons(msg: Message):
    r = await msg.answer('<b>Секунду...</b>')
    await r.edit_text(text=await tommorow.tommorow(msg))


@router.message(F.text == "хто я")
async def information(msg: Message):
    r = await msg.answer('<b>Секунду...</b>')
    await r.edit_text(text=await info.info(msg))


@router.message(F.text == "уроки сегодня")
async def information(msg: Message):
    r = await msg.answer('<b>Секунду...</b>')
    await r.edit_text(text=await lessonsToday.todaylessons(msg))


@router.message(F.text == 'Гдз запрос ура')
async def information(msg: Message):
    await msg.answer('<b>Секунду...</b>')
    dsadsd, orig= await recognize.recohniz(msg)
    await gdzAsking.asking(msg, dsadsd, orig)