import logging
from aiogram import Bot, Dispatcher
from bot.handlers import user, fsm
from bot.misc import TgKeys

async def start_bot():
    bot = Bot(token=TgKeys.TOKEN, parse_mode='HTML')
    dp = Dispatcher()
    dp.include_router(user.router)
    dp.include_router(fsm.router)
    logging.basicConfig(
    format='%(filename)s [LINE:%(lineno)d] #%(levelname)-8s [%(asctime)s]  %(message)s', level=logging.INFO)
    await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())
