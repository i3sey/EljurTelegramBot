import datetime


async def days_schedule():
        """Storage to schedule
        Returns:
            dict: schedule of currect day
        """

        """
        date = datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=5)))
        # class date:     debug
        #     hour = 22 
        #     minute = 16
        day = date.isoweekday()
        # day = 6
        if day in [1, 6, 7]:
            if (date.hour == 15 and date.minute >= 30) or (date.hour > 15):
                day += 1
        elif (date.hour == 14 and date.minute >= 55) or (date.hour > 14):
            day += 1
        return {
            '1': '08:45–09:25',
            '2': '09:30–10:10',
            '3': '10:25–11:05',
            '4': '11:25–12:05',
            '5': '12:25–13:05',
            '6': '13:15–13:55',
            '7': '14:05–14:45',
            '8': '14:50–15:30'
        } if day in [1, 6, 7] else {
            '1': '08:00–08:40',
            '2': '08:50–09:30',
            '3': '09:45–10:25',
            '4': '10:45–11:25',
            '5': '11:45–12:25',
            '6': '12:35–13:15',
            '7': '13:25–14:05',
            '8': '14:15–14:55'
        }"""
        return {
            '1': '08:00–08:40',
            '2': '08:50–09:30',
            '3': '09:45–10:25',
            '4': '10:45–11:25',
            '5': '11:45–12:25',
            '6': '12:35–13:15',
            '7': '13:25–14:05',
            '8': '14:15–14:55'
        }

async def sort_time(delta_times):
        """converts dict into list and sort it.
        Args:
            timeRem (dict): number of lesson : delta of times
        Returns:
            list: sorted list
        """
        temp_list = list(delta_times.items())
        deltas_list = [(val[0], val[1].seconds) for val in temp_list]
        deltas_list.sort(key=lambda i: i[1])
        return deltas_list

async def str_timing(sche_dict):
        """Find delta of currect time and times from dict
        Args:
            ScheDict (dict): dict with schedule
            utczone (pytz.timezone()): timezone
        Returns:
            dict: number of lesson : delta of times
        """
        time_delta = {}
        for i in sche_dict.items():
            now = datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=5)))
            from_sche = now.strptime(i[1], "%H:%M")
            delta_1 = datetime.timedelta(hours=now.hour,
                                minutes=now.minute,
                                seconds=now.second)
            delta_2 = datetime.timedelta(hours=from_sche.hour,
                                minutes=from_sche.minute,
                                seconds=from_sche.second)
            time_delta[i[0]] = (delta_2-delta_1)
        return time_delta

async def Tlschedule(message):
    """Конец/Начало близжайшего урока"""
    lessonStarts = {}
    lessonsEnds = {}
    temp = await days_schedule()
    for key, value in temp.items():
        lessonStarts[key] = value.split('–', maxsplit=1)[0]
        lessonsEnds[key] = value.split('–')[1]
    start = await sort_time(await str_timing(lessonStarts))
    end = await sort_time(await str_timing(lessonsEnds))
    now = datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=5)))
    if start[1][1] < end[1][1]:
        answer = f'До начала {start[0][0]} урока: <code>{datetime.datetime.utcfromtimestamp(start[0][1]).strftime("%H:%M:%S")}</code>\nУрок начнётся в <code>{str(lessonStarts[start[0][0]])}:00</code>'
    else:
        answer = f'До конца {end[0][0]} урока: <code>{datetime.datetime.utcfromtimestamp(end[0][1]).strftime("%H:%M:%S")}</code>\nУрок закончится в: <code>{str(lessonsEnds[end[0][0]])}:00</code>'
    await message.answer(answer)
