from aiogram import Bot, types
from aiogram.utils import executor
from aiogram.dispatcher import Dispatcher
from aiogram.types import ReplyKeyboardRemove, ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.dispatcher import FSMContext                            
from aiogram.dispatcher.filters import Command                        
from aiogram.contrib.fsm_storage.memory import MemoryStorage        
from aiogram.dispatcher.filters.state import StatesGroup, State        
import config
import keyboard
import logging
import api
import datetime

storage = MemoryStorage() # FOR FSM
bot = Bot(token=config.botkey, parse_mode=types.ParseMode.HTML)
dp = Dispatcher(bot, storage=storage)
logging.basicConfig(format=u'%(filename)s [LINE:%(lineno)d] #%(levelname)-8s [%(asctime)s]  %(message)s',level=logging.INFO,)

class userinfo(StatesGroup):
    QL = State()
    QP = State()
    QD = State()

def cleanup(dictionary):
    result = '\n'.join([f'{key.capitalize()}: {value}' for key, value in dictionary.items()])
    return result   


@dp.message_handler(Command("update"), state=None)
async def start(message: types.Message):
    await bot.send_message(message.chat.id, f"Кнопки были успешно обновлены!", reply_markup=keyboard.start, parse_mode='Markdown')

@dp.message_handler(Command("start"), state=None)
async def start(message: types.Message):
    joinedFile = open("user.txt","r")
    joinedUsers = set ()
    for line in joinedFile:
        joinedUsers.add(line.strip())

    if not str(message.chat.id) in joinedUsers:
        joinedFile = open("user.txt","a")
        joinedFile.write(str(message.chat.id)+ "\n")
        joinedUsers.add(message.chat.id)
    await message.answer('Привет, гони логин')
    await userinfo.QL.set()
    
@dp.message_handler(state=userinfo.QL)
async def login(message: types.Message, state: FSMContext):
    login = message.text
    await state.update_data(answer1=login)
    await message.answer('пароль дай')
    await userinfo.QP.set()
    
@dp.message_handler(state=userinfo.QP)
async def password(message: types.Message, state: FSMContext):
    password = message.text
    await state.update_data(answer2=password)
    await message.answer('домен дай')
    await userinfo.QD.set()
    
@dp.message_handler(state=userinfo.QD)
async def domain(message: types.Message, state: FSMContext):
    domain = message.text
    await state.update_data(answer3=domain)
    await message.answer('сек, чекаю')
    await userinfo.QD.set()
    
    data = await state.get_data()
    login = data.get("answer1") 
    password = data.get("answer2") 
    domain = data.get("answer3") 
    
    getter = api.newUser(message.chat.id, str(login), str(password), str(domain))
    if getter != 0:
        await message.answer('Произошла ошибка, убедитесь в праильности введённых данных')
        # Есть идея ещё код ошибки докинуть  TODO
        await message.answer('Привет, гони логин')
        await userinfo.QL.set()
    else:
        await bot.send_message(message.chat.id, f"ПРИВЕТ, *{str(api.idProfile(message.chat.id)['Имя'])},* БОТ РАБОТАЕТ", reply_markup=keyboard.start, parse_mode='Markdown')
        await state.finish()


@dp.message_handler(content_types=['text'])
async def get_message(message):
    match message.text:
        case "хто я":
            dictionary = api.idProfile(message.chat.id)
            result = cleanup(dictionary)
            await bot.send_message(message.chat.id,text=result, parse_mode='Markdown', reply_markup=keyboard.start)
        case 'предметы завтра':
            if datetime.datetime.today().weekday() == 6:
                dictionary = api.idJournal(message.chat.id, 1)
            else:
                dictionary = api.idJournal(message.chat.id, 0)
            #render
            dt = datetime.date.today() + datetime.timedelta(days=1)
            d = dt.strftime("%d")
            dt_string = dt.strftime(f"{d}.%m")
            for key, val in dictionary.items():
                if val['date'] == dt_string:
                        tommorowDay = key   
            if dictionary[tommorowDay]['isEmpty'] == True:
                lessones = 'Уроков нет, отдыхаем'
            else:
                lessones = cleanup(dictionary[tommorowDay]['lessons'])
            render = f'Завтра *{tommorowDay}, {dt_string}*\n{lessones}'                
            await bot.send_message(message.chat.id,text=render, parse_mode='Markdown', reply_markup=keyboard.start)
        case 'Список челов':
            await bot.send_message(message.chat.id, text = "Выберете категорию", reply_markup=keyboard.chels, parse_mode='Markdown')
            
            
            
@dp.callback_query_handler(text_contains='classruks')
async def classruks(call: types.CallbackQuery):
    r = api.peopleList('classruks')
    chelsa = InlineKeyboardMarkup()
    for key, val in r.items():
        chelsa.add(InlineKeyboardButton(f'{key}', callback_data = f'{val}'))
    chelsa.add(InlineKeyboardButton(f'◀️', callback_data = f'back'))
    await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text='Выбери:', reply_markup=chelsa)
    await bot.answer_callback_query(callback_query_id = call.id)
@dp.callback_query_handler(text_contains='administration')
async def administration(call: types.CallbackQuery):
    r = api.peopleList('administration')
    chelsa = InlineKeyboardMarkup()
    for key, val in r.items():
        chelsa.add(InlineKeyboardButton(f'{key}', callback_data = f'{val}'))
    chelsa.add(InlineKeyboardButton(f'◀️', callback_data = f'back'))
    await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text='Выбери:', reply_markup=chelsa)
    await bot.answer_callback_query(callback_query_id = call.id)
@dp.callback_query_handler(text_contains='specialists')
async def specialists(call: types.CallbackQuery):
    r = api.peopleList('specialists')
    chelsa = InlineKeyboardMarkup()
    for key, val in r.items():
        chelsa.add(InlineKeyboardButton(f'{key}', callback_data = f'{val}'))
    chelsa.add(InlineKeyboardButton(f'◀️', callback_data = f'back'))
    await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text='Выбери:', reply_markup=chelsa)
    await bot.answer_callback_query(callback_query_id = call.id)
@dp.callback_query_handler(text_contains='teachers')
async def teachers(call: types.CallbackQuery):
    r = api.peopleList('teachers')
    chelsa = InlineKeyboardMarkup()
    for key, val in r.items():
        chelsa.add(InlineKeyboardButton(f'{key}', callback_data = f'{val}'))
    chelsa.add(InlineKeyboardButton(f'◀️', callback_data = f'back'))
    await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text='Выбери:', reply_markup=chelsa)
    await bot.answer_callback_query(callback_query_id = call.id)
@dp.callback_query_handler(text_contains='parents')
async def parents(call: types.CallbackQuery):
    r = api.peopleList('parents')
    chelsa = InlineKeyboardMarkup()
    for key, val in r.items():
        chelsa.add(InlineKeyboardButton(f'{key}', callback_data = f'{val}'))
    chelsa.add(InlineKeyboardButton(f'◀️', callback_data = f'back'))
    await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text='Выбери:', reply_markup=chelsa)
    await bot.answer_callback_query(callback_query_id = call.id)
@dp.callback_query_handler(text_contains='students')
async def students(call: types.CallbackQuery):
    r = api.peopleList('students')
    chelsa = InlineKeyboardMarkup()
    for key, val in r.items():
        chelsa.add(InlineKeyboardButton(f'{key}', callback_data = f'{val}'))
    chelsa.add(InlineKeyboardButton(f'◀️', callback_data = f'back'))
    await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text='Выбери:', reply_markup=chelsa)
    await bot.answer_callback_query(callback_query_id = call.id)
    
    
    
    
@dp.callback_query_handler(text_contains='backc')
async def backc(call: types.CallbackQuery):
    for i in range(2):
            await bot.delete_message(call.message.chat.id, call.message.message_id-i)    
    
@dp.callback_query_handler(text_contains='back')
async def back(call: types.CallbackQuery):
    # await bot.delete_message(call.message.chat.id, call.message.message_id)
    await call.message.edit_text(text = "Выберете категорию", reply_markup=keyboard.chels, parse_mode='Markdown')
    # await bot.send_message(call.message.chat.id, text = "Выберете категорию", reply_markup=keyboard.chels, parse_mode='Markdown')
    
    

    
    
    
    
if __name__ == '__main__':
    print('Монстр пчелы запущен!')                                 
executor.start_polling(dp)