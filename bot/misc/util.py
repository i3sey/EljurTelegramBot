import datetime
from bot.api import idJournal, idProfile
from bot.misc.recognizer import finder


def cleanup(dictionary):
    return '\n'.join([f'<b>{key.capitalize() if isinstance(key, str) else " "}:</b> {value.capitalize() if isinstance(value, str) else " "}' for key, value in dictionary.items()])


def hwcleanup(dictionary):
    return '\n'.join([f'<b>{value["name"].capitalize()}:</b> {value["hometask"]}\n' for key, value in dictionary.items() if value["hometask"] is not None])


def dailyCleanup(dictionary):
    return '\n'.join([f'<b>{key.capitalize()}.</b> {value["name"].capitalize()}' for key, value in dictionary.items()])


async def lessones(msg):
    date_str, tommorow_day, lessone = await tommorow(msg)
    return f'Завтра <b>{tommorow_day}, {date_str}</b>\n{lessone}'


async def todaylessons(msg):
    time_zone = datetime.timezone(datetime.timedelta(hours=5))
    date = datetime.datetime.now(time_zone)
    day = date.strftime("%d")
    date_str = date.strftime(f"{day}.%m")
    dictionary = idJournal(msg.chat.id, 0)
    for key, val in dictionary.items():
        if val['date'] == date_str:
            today = key
            break
    return f'Сегодня <b>{today}, {date_str}</b>\n{dailyCleanup(dictionary[today]["lessons"])}'


async def tommorow(msg):
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
    day = date.strftime("%d")
    date_str = date.strftime(f"{day}.%m")
    for key, val in dictionary.items():
        if val['date'] == date_str:
            tommorow_day = key
            break
    if dictionary[tommorow_day]['isEmpty'] is True:
        lessone = 'Уроков нет, отдыхаем'
    else:
        lessone = dailyCleanup(dictionary[tommorow_day]['lessons'])
    return date_str, tommorow_day, lessone


async def info(msg):
    asa = idProfile(msg.chat.id)
    return cleanup(asa)


async def Homeworks(msg):
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
    day = date.strftime("%d")
    date_str = date.strftime(f"{day}.%m")
    for key, val in dictionary.items():
        if val['date'] == date_str:
            tommorow_day = key
            break
    if dictionary[tommorow_day]['isEmpty'] is True:
        lessone = 'Домашки, как и уроков нет, отдыхаем'
    else:
        lessone = hwcleanup(dictionary[tommorow_day]['lessons'])
    return f'Завтра <b>{tommorow_day}, {date_str}:</b>\n\n{lessone}'


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
    day = date.strftime("%d")
    date_str = date.strftime(f"{day}.%m")
    for key, val in dictionary.items():
        if val['date'] == date_str:
            tommorow_day = key
            break
    if dictionary[tommorow_day]['isEmpty'] is True:
        return -1
    res = [finder(value["hometask"], False)
           for key, value in dictionary[tommorow_day]['lessons'].items()]
