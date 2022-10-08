from bot.functions.api import idProfile
from bot.misc.util import cleanup


async def info(msg):
    asa = idProfile(msg.chat.id)
    return cleanup(asa)