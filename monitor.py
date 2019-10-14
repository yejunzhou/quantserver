import os
import sqlite3
import time
import traceback
from decimal import Decimal

import tushare as ts
import pandas as pd

from util import alert

pd.set_option('display.max_rows', 500)
pd.set_option('display.max_columns', 500)
pd.set_option('display.width', 1000)
import datetime

from sendmsg import sendmsg


def price2(price_max, price_min, current_price, name, wechate_account):
    if current_price >= price_max:
        sendmsg('上涨到价提醒：%s, 当前价格：%.2f, 设定价格：%.2f' % (name, current_price, price_max))
    elif current_price <= price_min:
        sendmsg('下跌到价提醒：%s, 当前价格：%.2f, 设定价格：%.2f' % (name, current_price, price_max))


def up_and_down(pre_close, current_price, percent_max, percent_min, name, wechate_account):
    ratio = (current_price - pre_close) * 100.0 / pre_close
    if ratio >= percent_max:
        sendmsg('上涨提醒：%s, 当前价格：%.2f, 涨幅超：%s%%' % (name, current_price, percent_max))
    elif ratio <= percent_min:
        sendmsg('下跌提醒：%s, 当前价格：%.2f, 跌幅超：%s%%' % (name, current_price, percent_min))


def profit_and_loss(cost, current_price, target_profit, stop_loss, name, wechate_account):
    ratio = (current_price - cost) * 100.0 / cost
    if ratio >= target_profit:
        sendmsg('上涨提醒：%s, 当前价格：%.2f, 涨幅超止盈线：%s%%' % (name, current_price, target_profit))
    elif ratio <= percent_min:
        sendmsg('下跌提醒：%s, 当前价格：%.2f, 跌幅超止损线：%s%%' % (name, current_price, stop_loss))


def check(code, base, price_max, price_min, percent_max, percent_min, percent_max_10,
          percent_min_10, cost, stop_loss, target_profit, wechate_account, rate, cache, is_first, cache_rate=None):
    time.sleep(1)
    df = ts.get_realtime_quotes(code)
    print(df)
    e = df[['code', 'name', 'price', 'pre_close', 'time']]
    p = df[u'price']
    open = float(df[[u'open']])
    pre_close = float(df[u'pre_close'])
    name = df[u'name'][0]
    print(e)
    current_price = float(p[0])
    if not base:
        base = current_price

    # todo 1:涨跌超过指定百分比报警，当前价格/昨日收盘价*100,取整，>1的整数倍报警；2：涨跌超过基准百分比报警
    rate = 1
    cache_rate, diff = alert(current_price, pre_close, cache_rate)
    if diff > 0 and diff >= rate:
        sendmsg('%s current:%.2f, more %.2f' % (name, p[0], diff), wechate_account)
    elif diff < 0 and diff <= rate:
        sendmsg('%s current:%.2f, less %.2f' % (name, p[0], diff), wechate_account)

    price2_key = 'price2_%s' % code
    if price2_key not in cache:
        price2(price_max, price_min, current_price, name, wechate_account)
        cache[price2_key] = 'alerted'
    up_and_down_key = 'up_and_down_%s' % code
    if up_and_down_key not in cache:
        up_and_down(pre_close, current_price, percent_max, percent_min, name, wechate_account)
        cache[up_and_down_key] = 'alerted'
    profit_and_loss_key = 'profit_and_loss_%s' % code
    if profit_and_loss_key not in cache:
        profit_and_loss(cost, current_price, target_profit, stop_loss, name, wechate_account)
        cache[profit_and_loss_key] = 'alerted'

    return base


def check2(code, wechate_account, cache_rate=None):
    time.sleep(1)
    df = ts.get_realtime_quotes(code)
    # print(df)
    e = df[['code', 'name', 'price', 'pre_close', 'time']]
    p = df[u'price']
    pre_close = float(df[u'pre_close'])
    name = df[u'name'][0]
    open_price = float(df['open'][0])
    # print(open_price)
    current_price = float(p[0])

    # todo 1:涨跌超过指定百分比报警，当前价格/昨日收盘价*100,取整，>1的整数倍报警；2：涨跌超过基准百分比报警
    current_rate, cache_rate, diff, is_alert = alert(current_price, pre_close, cache_rate)
    if diff > Decimal('0'):
        print('%s 当前价格:%.2f, 涨跌幅:%.2f, 上涨 %.2f' % (name, current_price, current_rate, diff))
    elif diff < Decimal('0'):
        print('%s 当前价格:%.2f, 涨跌幅:%.2f, 下跌 %.2f' % (name, current_price, current_rate, diff))
    if is_alert:
        if diff > Decimal('0'):
            sendmsg('%s 当前价格:%.2f, 涨跌幅:%.2f, 上涨 %.2f' % (name, current_price, current_rate, diff), wechate_account)
        else:
            sendmsg('%s 当前价格:%.2f, 涨跌幅:%.2f, 下跌 %.2f' % (name, current_price, current_rate, diff), wechate_account)

    return cache_rate


# price2(20.009, 10.112, 20.115, '测试')
# up_and_down(100, 150, 5, 3, '测试')
# up_and_down(100, 97, 5, 3, '测试')
# pre_close, current_price, percent_max, percent_min, name
# exit()
if __name__ == '__main__':
    tmp = {}
    while True:
        now = datetime.datetime.now()
        if (now.time() < datetime.time(hour=9, minute=25)) or (now.time() > datetime.time(hour=16)):
            time.sleep(1.01)
            print(now)
            continue
        conn = sqlite3.connect('db.sqlite3')
        c = conn.cursor()
        cursor = c.execute(
            "SELECT id, ticker,price_max,price_min,percent_max,percent_min,percent_max_10,percent_min_10,cost,stop_loss,target_profit,wechate_account  from remind_custom")
        for row in cursor:
            # print(row)
            ticker = str(row[1])
            price_max = float(row[2])
            price_min = float(row[3])
            percent_max = float(row[4])
            percent_min = float(row[5])
            percent_max_10 = float(row[6])
            percent_min_10 = float(row[7])
            cost = float(row[8])
            stop_loss = float(row[9])
            target_profit = float(row[10])
            wechate_account = row[11]
            try:
                if ticker not in tmp:
                    tmp[ticker] = check2(ticker, wechate_account, None)
                else:
                    tmp[ticker] = check2(ticker, wechate_account, tmp[ticker])
            except:
                traceback.print_exc()
                # sendmsg('exception')

        conn.close()
