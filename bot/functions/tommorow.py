import datetime

from bot.functions.api import idJournal
from bot.misc.util import dailyCleanup


async def tommorow(msg):
    urls = None
    time_zone = datetime.timezone(datetime.timedelta(hours=5))
    date = datetime.datetime.now(time_zone)
    if date.weekday() == 4:
        date += datetime.timedelta(days=3)
    elif date.weekday() == 5:
        date += datetime.timedelta(days=2)
    else:
        date += datetime.timedelta(days=1)
    today_week = datetime.datetime.now(time_zone).weekday()
    dictionary = idJournal(msg.chat.id, 1) if today_week in [
        6, 5, 4] else idJournal(msg.chat.id, 0)
    if dictionary == 1:
        return 'ошибка, попробуй войти с помощью команды /editData или напиши Денису'
    day = date.strftime("%d")
    date_str = date.strftime(f"{day}.%m")
    for key, val in dictionary.items():
        if val['date'] == date_str:
            tommorow_day = key
            break
    if dictionary[tommorow_day]['isEmpty'] is True:
        lessone = 'Уроков нет, отдыхаем'
    else:
        lessone, urls = dailyCleanup(dictionary[tommorow_day]['lessons'])
    return f'Завтра <b>{tommorow_day}, {date_str}</b>\n{lessone}', urls