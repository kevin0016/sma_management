"""
投资分析模块
包含业绩表现、业绩归因、风格分析等内容
"""

import datetime
import pandas as pd

from dateutil.relativedelta import relativedelta
from django.db.models import Max
from rest_framework.views import APIView, Response

from investment.models import (
    Income, IncomeAsset, ValuationBenchmark as VB, Holding, Balance, FundAdjPrice as FAP, TradingDays,
    FundPurchaseAndRedeem as FAR, StockIndustrySW as SISW
)
from investment.utils.calc import Formula
from investment.utils import fund, period_change as pc
from investment.utils.holding import fund_holding_stock


class PerformanceView(APIView):
    """业绩表现视图"""

    @staticmethod
    def get(request):
        date = request.query_params.get('date')
        port_code = request.query_params.get('portCode')
        if not date:
            date = datetime.date.today().strftime('%Y-%m-%d')
        p_nav = Income.objects.filter(port_code=port_code, date__lte=date).values('date', 'unit_nav')
        b_nav = VB.objects.filter(port_code=port_code, date__lte=date).values('date', 'unit_nav')
        p_nav = pd.DataFrame(p_nav).rename(columns={'unit_nav': 'p'})
        b_nav = pd.DataFrame(b_nav).rename(columns={'unit_nav': 'b'})
        data = pd.merge(p_nav, b_nav, on='date', how='inner').set_index('date')
        data = data.astype('float')
        ret = PerformanceView.calc_performance(data)
        return Response(ret)

    @staticmethod
    def calc_performance(data: pd.DataFrame):
        ret = {}

        for item in [
            "acc_return_yield",
            "annualized_return_yield",
            "daily_change",
            "trading_day_count",
            "annualized_volatility",
            "max_drawback",
            "sharpe_ratio",
            "calmar_ratio",
            "sortino_ratio",
            "var",
            "cvar"
        ]:
            n = getattr(Formula, item)(data).to_dict()
            ret.update({item: n})
        return ret


class AttributeChartView(APIView):
    """收益贡献图"""

    @staticmethod
    def get(request):
        date = request.query_params.get('date')
        port_code = request.query_params.get('portCode')
        if not date:
            date = datetime.date.today().strftime('%Y-%m-%d')
        d: IncomeAsset = IncomeAsset.objects.filter(port_code=port_code, date__lte=date).last()
        # a = Income.objects.filter(port_code=port_code, date__lte=date).last().net_asset
        cp = float(Income.objects.filter(port_code=port_code, date__lte=date).last().unit_nav) - 1
        a = d.total_profit
        data = {
            'total_profit': round(cp * 100, 2), 'equity': round(cp * float(d.equity/a) * 100, 2),
            'bond': round(cp*float(d.bond/a)*100, 2), 'alter': round(cp*float(d.alter/a)*100, 2),
            'moeny': round(cp*float(d.money/a)*100, 2)
        }
        return Response(data)


class FundHoldingView(APIView):
    """持有基金分析
    """

    @staticmethod
    def get(request):
        date = request.query_params.get('date')
        port_code = request.query_params.get('portCode')
        if not date:
            date = datetime.date.today().strftime('%Y-%m-%d')
        date = Holding.objects.filter(port_code=port_code, date__lte=date).aggregate(mdate=Max('date'))['mdate']
        holding = Holding.objects.filter(port_code=port_code, date=date).values('secucode', 'mkt_cap')
        na = Balance.objects.get(port_code=port_code, date=date).net_asset
        holding = pd.DataFrame(holding)

        holding['ratio'] = holding.mkt_cap / na
        holding = holding[holding['ratio'] > 0]
        holding = holding.sort_values(by=['ratio'], ascending=False).reset_index(drop=True)
        holding['key'] = holding.index + 1

        funds = list(set(list(holding.secucode)))
        names = fund.fund_names(funds)

        perf = FundHoldingView.period_return(funds, date)
        holding['secuname'] = holding.secucode.apply(lambda x: names.get(x))
        holding = pd.merge(holding, perf, on='secucode', how='left')

        limit = FundHoldingView.fund_limit(funds)
        holding = pd.merge(holding, limit, how='left', on='secucode')
        holding = holding.replace(pd.NA, None)

        holding = holding.to_dict(orient='records')
        return Response(holding)

    @staticmethod
    def period_return(funds: list, date: datetime.date):
        start = date - relativedelta(years=1, months=1)
        data = FAP.objects.filter(secucode__in=funds, date__range=[start, date]).values('secucode', 'adj_nav', 'date')
        data = pd.DataFrame(data)
        data.adj_nav = data.adj_nav.astype('float')
        data = pd.pivot_table(data, index='date', columns='secucode', values=['adj_nav'])['adj_nav']
        data = data.sort_index()
        tradingdays = TradingDays.objects.filter(date__range=[start, date]).values('date')
        tradingdays = [x['date'] for x in tradingdays]
        data = data[data.index.isin(tradingdays)]
        data.to_clipboard()
        p = pc.Performance(data)
        col = ['day', 'week', 'month', 'quarter', 'half_year', 'year', 'ytd']
        ret = []
        for attr in col:
            ret.append(getattr(p, attr)())
        ret = pd.concat(ret, axis=1)
        ret.columns = col
        ret = ret.reset_index()
        return ret

    @staticmethod
    def fund_limit(funds):
        date = FAR.objects.aggregate(mdate=Max('date'))['mdate']
        limit = FAR.objects.filter(secucode__in=funds, date=date).values(
            'secucode', 'apply_type', 'redeem_type', 'min_apply', 'max_apply'
        )
        limit = pd.DataFrame(limit)
        return limit


class FundHoldingStockView(APIView):
    @staticmethod
    def get(request):
        port_code = request.query_params.get('portCode')
        date = request.query_params.get('date')
        if not date:
            date = Balance.objects.filter(port_code=port_code).last().date.strftime('%Y-%m-%d')
        else:
            date = Balance.objects.filter(port_code=port_code, date__lte=date).last().date.strftime('%Y-%m-%d')
        ret = fund_holding_stock(port_code, date)
        ind = FundHoldingStockView.industry_sw(ret)
        ret = ret.to_dict(orient='records')
        ind = ind.to_dict(orient='records')
        return Response({'stock': ret, 'industry': ind})

    @staticmethod
    def industry_sw(data: pd.DataFrame) -> pd.DataFrame:
        """接受基金组合中股票市值占比的DataFrame"""
        funds = list(data.stockcode)
        ind = SISW.objects.filter(secucode__in=funds).values('secucode', 'firstindustryname')
        ind = pd.DataFrame(ind)
        ind = pd.merge(ind, data, left_on='secucode', right_on='stockcode')
        ind = ind.groupby(['firstindustryname'])['ratio'].sum()
        ind = ind.reset_index()
        ind = ind.sort_values(['ratio'], ascending=False)
        ind['ratioinequity'] = ind['ratio'] / ind['ratio'].sum()
        ind = ind.reset_index(drop=True)
        ind['key'] = ind.index + 1
        return ind
