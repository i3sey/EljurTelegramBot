from bot.functions.api import idProfile
from bot.misc.util import cleanup


async def info(msg):
    asa = idProfile(msg.chat.id)
    if asa == 1:
        return 'ошибка, попробуй войти с помощью команды /editData или напиши Денису'
    return cleanup(asa)