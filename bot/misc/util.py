import datetime
from bot.api import idJournal, idProfile

def cleanup(dictionary):
    return '\n'.join([f'<b>{key.capitalize()}:</b> {value.capitalize()}' for key, value in dictionary.items()])

def dailyCleanup(dictionary):
    return '\n'.join([f'<b>{key.capitalize()}.</b> {value["name"].capitalize()}' for key, value in dictionary.items()])

async def lessones(msg):
    time_zone = datetime.timezone(datetime.timedelta(hours=5))
    date = datetime.datetime.now(time_zone) + datetime.timedelta(days=1)
    if date.weekday() == 4:
        date += datetime.timedelta(days=3)
    if date.weekday() == 5:
        date += datetime.timedelta(days=2)
    elif date.weekday() == 6:
        date += datetime.timedelta(days=1)
    today_week = datetime.datetime.now(time_zone).weekday()
    dictionary = idJournal(msg.chat.id, 1) if today_week in [6, 5, 4] else idJournal(msg.chat.id, 0)
    day = date.strftime("%d")
    date_str = date.strftime(f"{day}.%m")
    for key, val in dictionary.items():
        if val['date'] == date_str:
            tommorow_day = key
    if dictionary[tommorow_day]['isEmpty'] is True:
        lessones = 'Уроков нет, отдыхаем'
    else:
        lessones = dailyCleanup(dictionary[tommorow_day]['lessons'])
    return f'Завтра <b>{tommorow_day}, {date_str}</b>\n{lessones}'

async def info(msg):
    asa = idProfile(msg.chat.id)
    return cleanup(asa)
