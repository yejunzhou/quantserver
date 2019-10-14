from django.contrib.auth.models import User
from django.db import models


# Create your models here.


class Custom(models.Model):
    ticker = models.CharField('ticker', help_text='股票代码', max_length=20)
    name = models.CharField('ticker_name', help_text='股票名称', max_length=20, null=True, blank=True)
    wechate_account = models.CharField('wechate_account', help_text='企业微信账户', max_length=20, default='yejunzhou')
    cost = models.FloatField('cost', help_text='成本价', default=0)
    price_max = models.FloatField('price_max', help_text='股价上涨到', null=True, blank=True)
    price_min = models.FloatField('price_min', help_text='股价下跌到', null=True, blank=True)
    percent_max = models.FloatField('percent_max', help_text='日涨幅超', null=True, blank=True)
    percent_min = models.FloatField('percent_min', help_text='日跌幅超', null=True, blank=True)
    stop_loss = models.FloatField('percent_min', help_text='止损线', default=0)
    target_profit = models.FloatField('percent_min', help_text='止盈线', default=0)
    percent_max_10 = models.BooleanField('percent_max_10', help_text='涨停', default=True)
    percent_min_10 = models.BooleanField('percent_min_10', help_text='跌停', default=True)
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    add_time = models.DateTimeField('add_time', help_text='添加时间', auto_now_add=True)
