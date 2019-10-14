import unittest
from decimal import Decimal

from util import alert


class TestDict(unittest.TestCase):
    def test_alert(self):
        rate = 1
        # 初始上涨3.5%，报警
        cache_rate, diff, is_alert = alert(10.35, 10, rate=rate)
        print(cache_rate, diff)
        self.assertEqual(cache_rate, Decimal('3.5'))
        self.assertTrue(is_alert)

        # 保持上一价格，不报警
        cache_rate, diff, is_alert = alert(10.35, 10, cache_rate)
        print(cache_rate, diff)
        self.assertEqual(diff, Decimal('0'))
        self.assertFalse(is_alert)

        # 上一价格基础上下跌0.5，不报警
        cache_rate, diff, is_alert = alert(10.30, 10, cache_rate)
        print(cache_rate, diff)
        self.assertEqual(diff, Decimal('-0.5'))
        self.assertFalse(is_alert)

        # 上一价格基础上下跌至1.1，报警
        cache_rate, diff, is_alert = alert(10.24, 10, cache_rate)
        print(cache_rate, diff)
        self.assertEqual(diff, Decimal('-1.1'))
        self.assertTrue(is_alert)

        # 上一价格基础上上涨2.2，报警
        cache_rate, diff, is_alert = alert(10.46, 10, cache_rate)
        print(cache_rate, diff)
        self.assertEqual(diff, Decimal('2.2'))
        self.assertTrue(is_alert)

        # 初始下跌3.5%，报警
        cache_rate, diff, is_alert = alert(9.65, 10, rate=rate)
        print(cache_rate, diff)
        self.assertEqual(diff, Decimal('-3.5'))
        self.assertTrue(is_alert)

        # 下跌2
        cache_rate, diff, is_alert = alert(9.45, 10, cache_rate)
        print(cache_rate, diff)
        self.assertEqual(diff, Decimal('-2'))
        self.assertTrue(is_alert)

        # 上一价格基础上上涨10.1，报警
        cache_rate, diff, is_alert = alert(10.46, 10, cache_rate)
        print(cache_rate, diff)
        self.assertEqual(diff, Decimal('10.1'))
        self.assertTrue(is_alert)

        # 上一价格基础上下跌0.1，不报警
        cache_rate, diff, is_alert = alert(10.45, 10, cache_rate)
        print(cache_rate, diff)
        self.assertEqual(diff, Decimal('-0.1'))
        self.assertFalse(is_alert)
