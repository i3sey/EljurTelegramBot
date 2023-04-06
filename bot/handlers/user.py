import datetime
from email.message import Message
import os

from aiogram import F, Router, types
from aiogram.fsm.context import FSMContext
from aiogram.utils.markdown import hide_link

from bot.classes.classes import UserInfo, loginMsg, FTA
from bot.database import main
from bot.database.main import BooksDB, filesDB
from bot.functions import (gdzAsking, hwSend, info, lessonsToday, recognize,
                           shedule, tommorow, tommorowHw, files)
from bot.functions.api import idKlass
from bot.keyboards import reply
from aiogram.types import FSInputFile
from bot.misc.util import urlcheck

router = Router()
dbm = BooksDB()
filesDB = filesDB()

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
    strings = [f"{str(key).capitalize()}: {item}" for key,
               item in items.items()]
    result = "\n".join(strings)
    await message.answer(result)


@router.message(commands=['bydit'])
async def bdnycmd(message: Message) -> None:
    await message.answer('Не будет')


@router.message(commands=['srs'])
async def srscmd(message: Message) -> None:
    await message.answer('srs')


@router.callback_query(text="nope")
async def cancel(callback_query):
    await callback_query.message.delete()


@router.callback_query(text="edit")
async def edit(msg: Message, state: FSMContext):
    await msg.answer('пока не воркает')


@router.callback_query(text="ok")
async def ok(callback_query, state: FSMContext):
    # await callback_query.answer('пока не воркает')
    pg = ''
    nm = ''
    mes, pg, nm, sj = await hwSend.hwSend(callback_query.message.html_text)
    r = await callback_query.message.answer(mes)
    await callback_query.message.delete()
    url = dbm.get(sj)
    if url != -1:
        await r.delete()
        if isinstance(nm, list):
            for n in nm:
                nonfileurl = urlcheck(url=url['nonfileurl'], pg=pg, nm=n)
                urld = urlcheck(url['url'], pg, n)
                await callback_query.message.answer(f'{hide_link(urld)}'
                                                    f'{nonfileurl}') 
        else:
            nonfileurl = urlcheck(url=url['nonfileurl'], pg=pg, nm=nm)
            urld = urlcheck(url['url'], pg, nm)
            await callback_query.message.answer(f'{hide_link(urld)}'
                                                    f'{nonfileurl}')
    else:
        await r.delete()
        await callback_query.message.answer('Я пока не умею этот предмет')

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
    text, urls = await tommorow.tommorow(msg)
    await r.delete()
    await msg.answer(text, reply_markup=reply.start)


@router.message(F.text == "хто я")
async def me(msg: Message):
    r = await msg.answer('<b>Секунду...</b>')
    text = await info.info(msg)
    await r.delete()
    await msg.answer(text, reply_markup=reply.start)


@router.message(F.text == "уроки сегодня")
async def lessonesToday(msg: Message):
    r = await msg.answer('<b>Секунду...</b>')
    text, urls = lessonsToday.todaylessons(msg)
    await msg.answer(text, reply_markup=reply.start)
    if urls:
        g = await msg.answer('Найдены файлы, скачиваю')
        send, firstSend = files.filesCheck(urls)
        if send:
            for file in send:
                await msg.answer_document(file['file_id'])
                FTA.FTAfiles.append(file)
            await g.delete()
        if firstSend:
            for file in firstSend:
                m = await msg.answer('Скачиваю этот файл в первый раз, пожалуйста ожидайте...')
                f = await msg.answer_document(FSInputFile(file['name'], filename=file['name']))
                file.update({'file_id': f.document.file_id})
                filesDB.add(file['name'],
                          file['file_id'],
                          file['hash'],
                          file['date'])
                os.remove(file['name'])
                await m.delete()
            await g.delete()
        # for g in t:
        #     msg.answer_document(FSInputFile(t, filename=t))
    await r.delete()

@router.message(F.text == 'Гдз запрос ура')
async def gdz(msg: Message):
    if idKlass(msg.chat.id) == '9':
        r = await msg.answer('<b>Секунду...</b>')
        result = await recognize.recohniz(msg)
        if result == -1:
            await r.edit_text(text='Домашки не нашёл')
            return
        dsadsd, orig = result
        if dsadsd == -99 and orig == -91:
            await r.edit_text(text='ошибка, попробуй войти с помощью команды /editData или напиши Денису')
        else:
            await r.delete()
            await gdzAsking.asking(msg, dsadsd, orig)
    else:
        await msg.answer('Для твоего класса пока недоступно')
        

