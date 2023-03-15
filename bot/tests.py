import unittest
from bot.functions import (info, shedule,
                           tommorow, tommorowHw)


class TestFunctions(unittest.IsolatedAsyncioTestCase):
    async def test_tommorow_lessons(self):
        class msg():
            class chat():
                id = '882076783'
        result = await tommorow.tommorow(msg)
        self.assertEqual(isinstance(result, str), True)

    async def test_tommorowHW(self):
        class msg():
            class chat():
                id = '882076783'
        result = await tommorowHw.Homeworks(msg)
        self.assertEqual(isinstance(result, str), True)

    async def test_info(self):
        class msg():
            class chat():
                id = '882076783'
        result = await info.info(msg)
        self.assertEqual(isinstance(result, str), True)

    async def test_sheduleTs(self):
        result = await shedule.days_schedule()
        self.assertEqual(isinstance(result, dict), True)


if __name__ == '__main__':
    unittest.main()
