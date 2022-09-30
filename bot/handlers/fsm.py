from aiogram.fsm.context import FSMContext
from aiogram import Router
from bot.handlers.user import UserInfo
from aiogram.types import Message
from bot.api import *
from bot.keyboards import inline

router = Router()

@router.message(UserInfo.QL)
async def EnterLogin(message: Message, state: FSMContext):
    await state.update_data(EnteredLogin=message.text)
    await message.answer(text='пароль дай')
    await state.set_state(UserInfo.QP)

@router.message(UserInfo.QP)
async def EnterPassword(message: Message, state: FSMContext):
    await state.update_data(EnteredPassword=message.text)
    await message.answer(text='домен дай')
    await state.set_state(UserInfo.QD)

@router.message(UserInfo.QD)
async def EnterDomain(message: Message, state: FSMContext):
    await state.update_data(EnteredDomain=message.text)
    await message.answer('сек, чекаю')
    await finishRegistration(message, state)
    
async def finishRegistration(message, state):
    data = await state.get_data()
    getter = newUser(message.chat.id, data['EnteredLogin'],
                         data['EnteredPassword'], data['EnteredDomain'])
    if getter != 0:
        await message.answer('Произошла ошибка, убедитесь в праильности введённых данных')
        # Есть идея ещё код ошибки докинуть  TODO
        await message.answer('Привет, гони логин')
        await state.set_state(UserInfo.QL)
    else:
        await message.answer(f"ПРИВЕТ, *{idProfile(message.chat.id)['Имя']},* БОТ РАБОТАЕТ",reply_markup=inline.start)
        await state.clear()