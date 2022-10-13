from email.message import Message

from aiogram import F, Router, types
from aiogram.fsm.context import FSMContext

from bot.classes.classes import UserInfo, loginMsg
from bot.database import main
from bot.functions import (gdzAsking, info, lessonsToday, recognize, tommorow,
                           tommorowHw)
from bot.keyboards import reply

router = Router()

@router.message(commands=["editData"])
async def editReg(msg: Message, state: FSMContext):
    loginMsg.msg = await msg.answer('Привет, гони логин')
    await state.set_state(UserInfo.QL)

@router.callback_query(text="nope")
async def cancel(msg: Message, state: FSMContext):
    await msg.answer('пока не воркает')

@router.callback_query(text="edit")
async def cancel(msg: Message, state: FSMContext):
    await msg.answer('пока не воркает')

@router.callback_query(text="ok")
async def cancel(msg: Message, state: FSMContext):
    await msg.answer('пока не воркает')

# @router.message(commands=["reset"])
# async def update(msg: Message):
#     main.DiaryDB('database.db').resetdb()
#     await msg.answer("Кнопки были успешно обновлены!", reply_markup=reply.start)


@router.message(commands=["start"])
async def start(msg: types.Message, state: FSMContext):
    PeopleId = main.DiaryDB('database.db').get(f'{msg.chat.id}_login')
    if PeopleId == False:
        loginMsg.msg = await msg.answer('Привет, гони логин')
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
    r = await msg.answer('<b>Секунду...</b>')
    dsadsd, orig= await recognize.recohniz(msg)
    if dsadsd == -99 and orig == -91:
        await r.edit_text(text='ошибка, попробуй войти с помощью команды /editData или напиши Денису')
    else:
        await r.delete()
        await gdzAsking.asking(msg, dsadsd, orig)