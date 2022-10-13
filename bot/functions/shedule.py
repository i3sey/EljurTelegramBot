import datetime


async def days_schedule():
        """Storage to schedule
        Returns:
            dict: schedule of currect day
        """
        date = datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=5)))
        day = date.isoweekday()
        return {
            '1': '08:35–09:15',
            '2': '09:25–10:05',
            '3': '10:20–11:00',
            '4': '11:20–12:00',
            '5': '12:20–13:00',
            '6': '13:10–13:50',
            '7': '14:00–14:40',
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
