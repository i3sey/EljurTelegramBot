import datetime
from email.message import Message

from aiogram import F, Router, types
from aiogram.fsm.context import FSMContext

from bot.classes.classes import UserInfo, loginMsg
from bot.database import main
from bot.functions import (gdzAsking, info, lessonsToday, recognize, shedule,
                           tommorow, tommorowHw, hwSend)
from bot.keyboards import reply

router = Router()

@router.message(commands=["editData"])
async def editReg(msg: Message, state: FSMContext):
    loginMsg.msg = await msg.answer('Привет, гони логин')
    await state.set_state(UserInfo.QL)

@router.message(commands=['tl'])
async def tlcmd(message: Message) -> None:
        await shedule.Tlschedule(message)

@router.message(commands=['ts'])
async def tscmd(message: Message) -> None:
    """Текущее расписание на день"""
    items = await shedule.days_schedule()
    strings = [f"{str(key).capitalize()}: {item}" for key, item in items.items()]
    result = "\n".join(strings)
    await message.answer(result)

@router.message(commands=['bydit'])
async def bdnycmd(message: Message) -> None:
    await message.answer('Не будет')

@router.message(commands=['y'])
async def srscmd(message: Message) -> None:
    await message.answer('🎰')

@router.callback_query(text="nope")
async def cancel(msg: Message, state: FSMContext):
    await msg.answer('пока не воркает')

@router.callback_query(text="edit")
async def edit(msg: Message, state: FSMContext):
    await msg.answer('пока не воркает')

@router.callback_query(text="ok")
async def ok(callback_query, state: FSMContext):
    await callback_query.answer('пока не воркает')
    mes, pg, nm, sj = await hwSend.hwSend(callback_query.message.html_text)
    r = await callback_query.message.answer(mes)
    if sj == 'физика':
        await r.delete()
        await callback_query.message.answer(f'гдз по Физике: https://reshak.ru/reshebniki/fizika/9/perishkin/images1/new/Upr/{int(nm)+4 if int(nm)>20 else nm}.png')
    

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
async def homeworkTM(msg: Message):
    r = await msg.answer('<b>Секунду...</b>')
    text = await tommorowHw.Homeworks(msg)
    await r.delete()
    await msg.answer(text, reply_markup=reply.start)


@router.message(F.text == "предметы завтра")
async def lessonsTommorow(msg: Message):
    r = await msg.answer('<b>Секунду...</b>')
    text=await tommorow.tommorow(msg)
    await r.delete()
    await msg.answer(text, reply_markup=reply.start)


@router.message(F.text == "хто я")
async def me(msg: Message):
    r = await msg.answer('<b>Секунду...</b>')
    text=await info.info(msg)
    await r.delete()
    await msg.answer(text, reply_markup=reply.start)


@router.message(F.text == "уроки сегодня")
async def lessonesToday(msg: Message):
    r = await msg.answer('<b>Секунду...</b>')
    text=await lessonsToday.todaylessons(msg)
    await r.delete()
    await msg.answer(text, reply_markup=reply.start)

@router.message(F.text == 'Гдз запрос ура')
async def gdz(msg: Message):
    r = await msg.answer('<b>Секунду...</b>')
    dsadsd, orig= await recognize.recohniz(msg)
    if dsadsd == -99 and orig == -91:
        await r.edit_text(text='ошибка, попробуй войти с помощью команды /editData или напиши Денису')
    else:
        await r.delete()
        await gdzAsking.asking(msg, dsadsd, orig)
