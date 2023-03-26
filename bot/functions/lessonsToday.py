import datetime
from bot.functions.api import idJournal
from bot.misc.util import dailyCleanup

def todaylessons(msg):
    time_zone = datetime.timezone(datetime.timedelta(hours=5))
    date = datetime.datetime.now(time_zone)
    day = date.strftime("%d")
    date_str = date.strftime(f"{day}.%m")
    dictionary = idJournal(msg.chat.id, 0)
    if dictionary == 1:
        return 'ошибка, попробуй войти с помощью команды /editData или напиши Денису'
    today = next((key for key, val in dictionary.items() if val['date'] == date_str), None)
    if today:    
        lessone, urls = dailyCleanup(dictionary[today]["lessons"])
        return f'Сегодня <b>{today}, {date_str}</b>\n{lessone}', urls
    else:
        return f'Уроков нет', {}