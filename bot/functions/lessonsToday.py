import datetime

from bot.functions.api import idJournal
from bot.misc.util import dailyCleanup


async def todaylessons(msg):
    time_zone = datetime.timezone(datetime.timedelta(hours=5))
    date = datetime.datetime.now(time_zone)
    day = date.strftime("%d")
    date_str = date.strftime(f"{day}.%m")
    dictionary = idJournal(msg.chat.id, 0)
    if dictionary == 1:
        return 'ошибка, попробуй войти с помощью команды /editData или напиши Денису'
    for key, val in dictionary.items():
        if val['date'] == date_str:
            today = key
            break
    return f'Сегодня <b>{today}, {date_str}</b>\n{dailyCleanup(dictionary[today]["lessons"])}'