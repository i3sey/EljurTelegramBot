from email.message import Message
from aiogram import F, Router, types
from aiogram.filters import CommandObject
from bot.functions import updatee
from bot.database.main import BooksDB

router = Router()
dbm = BooksDB()

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
            await msg.answer('pg и nm')
@router.message(commands=['e'])
async def addbook(msg: Message, command: CommandObject) -> None:
    if msg.chat.id == 882076783:
        if command.args:
            eval(command.args)
            await msg.answer('done')
