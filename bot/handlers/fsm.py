from aiogram import Router
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message

from bot.classes.classes import UserInfo, loginMsg
from bot.functions.api import idProfile, newUser
from bot.functions.gdzAsking import GdzAsking
from bot.handlers.user import UserInfo
from bot.keyboards import reply

router = Router()


@router.message(UserInfo.QL)
async def EnterLogin(message: Message, state: FSMContext):
    await state.update_data(EnteredLogin=message.text)
    await message.delete()
    await loginMsg.msg.edit_text(text='пароль дай')
    await state.set_state(UserInfo.QP)


@router.message(UserInfo.QP)
async def EnterPassword(message: Message, state: FSMContext):
    await state.update_data(EnteredPassword=message.text)
    await message.delete()
    await loginMsg.msg.edit_text(text='домен дай')
    await state.set_state(UserInfo.QD)


@router.message(UserInfo.QD)
async def EnterDomain(message: Message, state: FSMContext):
    await state.update_data(EnteredDomain=message.text)
    await message.delete()
    await loginMsg.msg.edit_text('сек, чекаю')
    await finishRegistration(message, state)

# @router.message(GdzAsking.nope)
# async def nope(callback: CallbackQuery, state: FSMContext):
#     await callback.message.answer('dsdsdsdsdsdsdsd')

async def finishRegistration(message, state):
    data = await state.get_data()
    getter = newUser(message.chat.id, data['EnteredLogin'],
                     data['EnteredPassword'], data['EnteredDomain'])
    if getter != 0:
        await loginMsg.msg.answer('Произошла ошибка, убедитесь в праильности введённых данных')
        # Есть идея ещё код ошибки докинуть  TODO
        loginMsg.msg = await message.answer('Привет, гони логин')
        await state.set_state(UserInfo.QL)
    else:
        await loginMsg.msg.answer(f"привет, <b>{idProfile(message.chat.id)['Имя']},</b> бот работает ура", reply_markup=reply.start)
        await state.clear()
