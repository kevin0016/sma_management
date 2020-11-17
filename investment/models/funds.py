"""
fund
~~~~~~~~~~~~~~~~~~~~~~~
@author: chuanchao.peng
@date: 2020-06-30
@desc: 定义基金基础数据model
"""

from django.db import models
from django.utils import timezone


# 基金列表
class Funds(models.Model):
    secucode = models.CharField(max_length=12, primary_key=True, verbose_name='基金代码')
    secuname = models.CharField(max_length=50, verbose_name='基金简称')

    class Meta:
        db_table = "sma_funds"
        verbose_name = '基金主表'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.secucode


# 基金净值或万份收益数据
class FundPrice(models.Model):
    secucode = models.ForeignKey(Funds, to_field='secucode', on_delete=models.CASCADE)
    nv = models.DecimalField(verbose_name='净资产值(元)', null=True, max_digits=18, decimal_places=4)
    nav = models.DecimalField(verbose_name='单位净值', max_digits=18, decimal_places=6, null=True, blank=True)
    acc_nav = models.DecimalField(verbose_name='累计单位净值', max_digits=18, decimal_places=6, null=True, blank=True)
    dailyprofit = models.DecimalField(verbose_name='万份收益', null=True, max_digits=18, decimal_places=6, blank=True)
    date = models.DateField(verbose_name='交易日', null=False, default=timezone.now)

    class Meta:
        db_table = 'sma_fund_price'
        verbose_name = '基金累计净值表'
        verbose_name_plural = verbose_name
        index_together = ['secucode', 'date']
        get_latest_by = ['date']

    def __str__(self):
        return f'{self.secucode.secucode} {self.secucode.secuname}'


# 基金复权净值
class FundAdjPrice(models.Model):
    secucode = models.ForeignKey(Funds, to_field='secucode', on_delete=models.CASCADE)
    nav = models.DecimalField(verbose_name='单位净值', max_digits=18, decimal_places=6, null=True, blank=True)
    adj_nav = models.DecimalField(verbose_name='累计单位净值', max_digits=18, decimal_places=6, null=True, blank=True)
    date = models.DateField(verbose_name='交易日', null=False, default=timezone.now)

    class Meta:
        db_table = 'sma_fund_adj_price'
        verbose_name = '基金复权单位净值表'
        verbose_name_plural = verbose_name
        index_together = ['secucode', 'date']
        get_latest_by = ['date']

    def __str__(self):
        return f'{self.secucode.secucode} {self.secucode.secuname}'


# 基金风格
class FundStyle(models.Model):
    secucode = models.ForeignKey(Funds, to_field='secucode', on_delete=models.CASCADE)
    fundstyle = models.CharField(max_length=20, verbose_name="基金投资风格")
    fundtype = models.CharField(max_length=20, verbose_name="基金类型")

    class Meta:
        db_table = "sma_fund_style"
        verbose_name = "基金风格"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.secucode.secuname


# 基金申赎状态
class FundPurchaseAndRedeem(models.Model):
    secucode = models.ForeignKey(Funds, to_field='secucode', on_delete=models.CASCADE)
    apply_type = models.CharField(verbose_name='申购状态', null=True, max_length=20)
    redeem_type = models.CharField(verbose_name='赎回状态', null=True, max_length=20)
    min_apply = models.DecimalField(verbose_name='购买起点', max_digits=18, decimal_places=2, null=True, max_length=20)
    max_apply = models.DecimalField(verbose_name='单日限额', max_digits=18, decimal_places=2, null=True, max_length=20)
    date = models.DateField(auto_now=True)

    class Meta:
        db_table = "sma_fund_purchase_and_redeem"
        verbose_name = "基金申赎状态"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.secucode.secucode


# 基金持股
class FundHoldingStock(models.Model):
    secucode = models.ForeignKey(Funds, to_field='secucode', on_delete=models.CASCADE, verbose_name='基金代码')
    stockcode = models.CharField(max_length=20, null=False, verbose_name='股票代码')
    stockname = models.CharField(max_length=20, null=False, verbose_name='股票简称')
    serial = models.IntegerField(verbose_name='排名', null=False, default=1)
    ratio = models.DecimalField(verbose_name='占净值比', decimal_places=4, max_digits=8, default=0)
    date = models.DateField(verbose_name='报告期')

    class Meta:
        db_table = "sma_fund_holding_stock"
        verbose_name = "基金持股情况"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.secucode.secucode
