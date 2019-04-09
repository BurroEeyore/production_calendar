import unittest
from datetime import datetime, date

from date_utils import Days


class TestDaysMethods(unittest.TestCase):
    def test_is_relax_day(self):
        d = Days()
        day = datetime(year=2019, month=1, day=1, hour=1, minute=0, second=0, microsecond=0)
        self.assertEqual(d.is_relax_day(day), True)

        day = date(year=2019, month=1, day=1)
        self.assertEqual(d.is_relax_day(day), True)

        day = datetime(year=2019, month=3, day=7, hour=1, minute=0, second=0, microsecond=0)
        self.assertEqual(d.is_relax_day(day), False)

        day = '2019-01-01'
        self.assertEqual(d.is_relax_day(day), None)

        day = date(year=1999, month=1, day=1)
        self.assertEqual(d.is_relax_day(day), None)

    def test_get_next_day(self):
        d = Days()
        day = datetime(year=2019, month=1, day=1, hour=1, minute=0, second=0, microsecond=0)
        next_day = datetime(year=2019, month=1, day=2, hour=1, minute=0, second=0, microsecond=0)
        self.assertEqual(d.get_next_day(day=day, is_work=False), next_day)

        day = datetime(year=2019, month=1, day=1, hour=1, minute=0, second=0, microsecond=0)
        next_day = datetime(year=2019, month=1, day=9, hour=1, minute=0, second=0, microsecond=0)
        self.assertEqual(d.get_next_day(day=day, is_work=True), next_day)

    def test_get_count_days(self):
        d = Days()
        d_from = datetime(year=2019, month=1, day=1, hour=1, minute=0, second=0, microsecond=0)
        d_till = datetime(year=2019, month=1, day=10, hour=1, minute=0, second=0, microsecond=0)
        result = {'work': 2, 'relax': 8, 'calendar': 10}
        self.assertEqual(d.get_count_days(date_from=d_from, date_till=d_till), result)

        d_from = datetime(year=2019, month=1, day=1, hour=1, minute=0, second=0, microsecond=0)
        d_till = datetime(year=2019, month=1, day=1, hour=1, minute=0, second=0, microsecond=0)
        result = {'work': 0, 'relax': 1, 'calendar': 1}
        self.assertEqual(d.get_count_days(date_from=d_from, date_till=d_till), result)

        d_from = datetime(year=2019, month=1, day=10, hour=1, minute=0, second=0, microsecond=0)
        d_till = datetime(year=2019, month=1, day=1, hour=1, minute=0, second=0, microsecond=0)
        result = {'work': 0, 'relax': 1, 'calendar': 1}
        self.assertEqual(d.get_count_days(date_from=d_from, date_till=d_till), result)

        d_from = datetime(year=2018, month=1, day=1, hour=1, minute=0, second=0, microsecond=0)
        d_till = datetime(year=2019, month=1, day=1, hour=1, minute=0, second=0, microsecond=0)
        result = {'work': 0, 'relax': 1, 'calendar': 366}
        self.assertEqual(d.get_count_days(date_from=d_from, date_till=d_till), result)

if __name__ == '__main__':
    unittest.main()
