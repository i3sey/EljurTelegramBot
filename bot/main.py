import logging
from aiogram import Bot, Dispatcher
from bot.handlers import user, fsm, admin
from bot.misc import TgKeys


async def start_bot():  # define an asynchronous function called "start_bot"
    # create an instance of the telegram bot and specify its token and mode for parsing messages
    bot = Bot(token=TgKeys.TOKEN, parse_mode='HTML')
    dp = Dispatcher()  # create an instance of the telegram bot's dispatcher
    # add a router for handling user commands to the dispatcher
    dp.include_router(admin.router)
    # add a router for handling user commands to the dispatcher
    dp.include_router(user.router)
    # add a router for handling finite state machine callbacks to the dispatcher
    dp.include_router(fsm.router)
    logging.basicConfig(  # configure the logging module to format log messages with specific information such as date/time and severity level
        format='%(filename)s [LINE:%(lineno)d] #%(levelname)-8s [%(asctime)s]  %(message)s', level=logging.INFO)
    # start polling the telegram API for new messages and updates using the given bot instance and update types specified by the dispatcher
    await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())
