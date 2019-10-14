from decimal import Decimal


def alert(current_price, pre_close, cache_rate=None, rate=1.0):
    is_alert = False
    current_price = Decimal(str(current_price))
    pre_close = Decimal(str(pre_close))
    current_rate = (current_price - pre_close) / pre_close * 100
    if cache_rate:
        diff = current_rate - cache_rate
    else:
        diff = current_rate
    if diff > Decimal(str(rate)):
        # print('上涨：%s' % diff)
        cache_rate = current_rate
        is_alert = True
    elif diff < Decimal(str(-rate)):
        # print('下跌：%s' % diff)
        cache_rate = current_rate
        is_alert = True
    return current_rate,cache_rate, diff, is_alert


if __name__ == '__main__':
    pre_close = 6.750
    current_price = 6.500

    price_ = (pre_close - current_price)
    close___ = price_ / pre_close * 100.0
    r = close___ // 1
    print(price_)
    print(close___)
    print(r)
