from aiogram.types import Message
from aiogram.filters.state import State, StatesGroup
from bot.keyboards import inline

class GdzAsking(StatesGroup):
    nope = State()

async def asking(msg: Message, dictq, orig):
    for key, value in dictq.items():
        await msg.answer(text=f'Я обнаружил домашку по предмету <b>{key}</b>\nЧто написано в дневнике: <code><i>{orig[key]}</i></code>\nЧто я распознал: <code>{value}</code>', reply_markup=inline.keyboard)