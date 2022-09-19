from aiogram import Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.types import Message
from bot.handlers.user.main import UserInfo
from bot.api import *
from bot.keyboards import inline

# async def echo(msg: Message):
#     # todo: remove echo example:3
#     await msg.answer(msg.text)

async def login(message: Message, state: FSMContext):
    user_login = message.text
    await state.update_data(answer1=user_login)
    await message.answer('пароль дай')
    await UserInfo.QP.set()
    
async def password(message: Message, state: FSMContext):
    user_password = message.text
    await state.update_data(answer2=user_password)
    await message.answer('домен дай')
    await UserInfo.QD.set()
    
async def domain(message: Message, state: FSMContext):
    user_domain = message.text
    await state.update_data(answer3=user_domain)
    await message.answer('сек, чекаю')
    await finishRegistration(message, state)

async def finishRegistration(message, state):
    data = await state.get_data()

    getter = newUser(message.chat.id, str(data.get("answer1")),
                         str(data.get("answer2")), str(data.get("answer3")))
    if getter != 0:
        await message.answer('Произошла ошибка, убедитесь в праильности введённых данных')
        # Есть идея ещё код ошибки докинуть  TODO
        await message.answer('Привет, гони логин')
        await UserInfo.QL.set()
    else:
        await message.answer(f"ПРИВЕТ, *{idProfile(message.chat.id)['Имя']},* БОТ РАБОТАЕТ",reply_markup=inline.start)
        await state.finish()

def register_other_handlers(dp: Dispatcher) -> None:
    # todo: register all other handlers
    # dp.register_message_handler(echo, content_types=['text'])
    dp.register_message_handler(login, state=UserInfo.QL)
    dp.register_message_handler(password, state=UserInfo.QP)
    dp.register_message_handler(domain, state=UserInfo.QD)
