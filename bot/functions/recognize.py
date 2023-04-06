import datetime
import re

from bot.functions.api import idJournal
from bot.misc.util import magicLoop, merge


async def recohniz(msg):
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
        return -99, -91
    day = date.strftime("%d")
    date_str = date.strftime(f"{day}.%m")
    for key, val in dictionary.items():
        if val['date'] == date_str:
            tommorow_day = key
            break
    if dictionary[tommorow_day]['isEmpty'] is True:
        return -1
    i = {}
    y = {}
    for key, value in dictionary[tommorow_day]['lessons'].items():
        a = finder(value["hometask"], False)
        if a is None:
            continue
        i[value["name"]] = a
        y[value["name"]] = value["hometask"]
    return i, y


def finder(hometask, splitBool):
    page = (
        'стр',
        'страница',
        'с',
        '§'
    )
    number = (
        'номер',
        'упр',
        'упражнение',
        '№'
    )
    if splitBool == True:
        f = re.sub(r'(?<=\d)(?!\d)|(?<!\d)(?=\d)', ' ', hometask)
        lst = f.replace('.', '').replace(',', ' ').split()
    else:
        try:
            lst = hometask.replace(',', ' ').split()
        except AttributeError:
            return
    ist = [i.lower() for i in lst]
    PageLetter = magicLoop(ist, page)
    NumLetter = magicLoop(ist, number)
    if PageLetter == -2 and NumLetter != -2:
        return {'number': merge(ist, NumLetter)}
    elif NumLetter == -2 and PageLetter != -2:
        return {'page': merge(ist, PageLetter)}
    elif PageLetter == -2:
        return finder(hometask, True) if splitBool == False else None
    else:
        return {'page': merge(ist, PageLetter), 'number': merge(ist, NumLetter)}
