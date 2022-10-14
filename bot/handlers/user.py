import datetime
from email.message import Message

from aiogram import F, Router, types
from aiogram.fsm.context import FSMContext

from bot.classes.classes import UserInfo, loginMsg
from bot.database import main
from bot.functions import (gdzAsking, info, lessonsToday, recognize, shedule,
                           tommorow, tommorowHw)
from bot.keyboards import reply

router = Router()

@router.message(commands=["editData"])
async def editReg(msg: Message, state: FSMContext):
    loginMsg.msg = await msg.answer('Привет, гони логин')
    await state.set_state(UserInfo.QL)

@router.message(commands=['tl'])
async def tlcmd(message: Message) -> None:
        """Конец/Начало близжайшего урока"""
        lessonStarts = {}
        lessonsEnds = {}
        temp = await shedule.days_schedule()
        for key, value in temp.items():
            lessonStarts[key] = value.split('–', maxsplit=1)[0]
            lessonsEnds[key] = value.split('–')[1]
        start = await shedule.sort_time(await shedule.str_timing(lessonStarts))
        end = await shedule.sort_time(await shedule.str_timing(lessonsEnds))
        now = datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=5)))
        if start[1][1] < end[1][1]:
            answer = f'До начала {start[0][0]} урока: <code>{datetime.datetime.utcfromtimestamp(start[0][1]).strftime("%H:%M:%S")}</code>\nУрок начнётся в <code>{str(lessonStarts[start[0][0]])}:00</code>'
        else:
            answer = f'До конца {end[0][0]} урока: \nУрок закончится в: <code>{str(lessonsEnds[end[0][0]])}:00</code>'
        await message.answer(answer)

@router.message(commands=['ts'])
async def tscmd(message: Message) -> None:
    """Текущее расписание на день"""
    items = await shedule.days_schedule()
    strings = [f"{str(key).capitalize()}: {item}" for key, item in items.items()]
    result = "\n".join(strings)
    await message.answer(result)

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
