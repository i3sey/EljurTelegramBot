import datetime
from email.message import Message
import hashlib
import os
from aiogram import F, Router, types
from aiogram.filters import CommandObject
from bot.functions import updatee
from bot.database.main import BooksDB, filesDB
from bot.classes.classes import FTA
from bot.misc.util import download, calculate_hash

router = Router()
dbm = BooksDB()
fdb = filesDB()
# Routes updates telegram bot command 'update' to this function using decorator.
@router.message(commands=['update'])
# Asynchronous function declaration with message object as arguement and returning None.
async def update(message: Message) -> None:
    # Checking if message is coming from chat with specific chat ID.
    if message.chat.id == 882076783:
        # If yes then calling the `updateq()` and sending its output in HTML code format.
        await message.answer(f'<code>{updatee.updateq()}</code>' if updatee.updateq() else 'no')

@router.message(commands=['add'])
async def addbook(msg: Message, command: CommandObject) -> None:
    if msg.chat.id == 882076783:
        if command.args:
            data = command.args.split(';')
            dbm.add(data[0], data[1], data[2])
            await msg.answer('done')
        else:
            msg.answer('pg и nm')
            
@router.message(commands=['startwatch'])
async def filesUpdate(msg: Message):
    if msg.chat.id == 882076783:
        urls = []
        new_files_list = []
        problems = 0
        extime = 0
        count = 0
        for file in FTA.FTAfiles:
            if file['url'] not in urls:
                urls.append(file['url'])
                new_files_list.append(file)
        
        for g in new_files_list:
            download(g['url'], 'temp')
            rez = calculate_hash('temp')
            rez2 = fdb.getID(g['file_id'])['hash']
            if rez != rez2:
                problems+=1
                fdb.delete(g['file_id'])
                os.remove('temp')
                continue
            date1 = fdb.getID(g['file_id'])['date']
            date2 = datetime.datetime.now()
            delta = date2 - date1
            if delta.days >= 14:
                extime+=1
                fdb.delete(g['file_id'])
            os.remove('temp')
            count+=1
        await msg.answer(f'Цикл выполнен {count} раз! Несоответствий: {problems}\nИстекло времени: {extime}')