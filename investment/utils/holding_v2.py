"""
holding
~~~~~~~
@date: 2021-08-06
@desc: v2版，加入私私募，后续会加入股票、债券
私募视为另类资产，ETF、股票视为权益资产，债券视为固收资产
"""
import datetime

from django.db.models import Subquery

from investment import models


def security_asset_type(secucode):
    """证券的穿透资产类型"""
    security = models.Security.objects.filter(secucode=secucode).first()
    # 证券主表中查询不到该证券 可能为货基或是买入返售金融资产
    if not security:
        return open_fund_asset_type(secucode)
    if security.category_code in ('110503', '110504'):
        return {'equity': 1}
    elif security.category_code in ('110508', '110906'):
        return {'alternative': 1}
    elif security.category_code == '110502':
        return open_fund_asset_type(secucode)
    return {'other': 1}


def open_fund_asset_type(secucode):
    """开放式基金穿透资产配置"""
    secucode = open_fund_maincode(secucode)
    try:
        rpt = models.FundAssetAllocate.objects.filter(secucode=secucode).latest('date')
    except models.FundAssetAllocate.DoesNotExist:
        return {'other': 1}
    asset = models.FundAssetAllocate.objects.filter(secucode=secucode, date=rpt.date).last()
    ratio = {
        'equity': asset.stock, 'fix_income': asset.bond, 'alternative': asset.metals, 'monetary': asset.monetary,
        'other': asset.other
    }
    return ratio


def open_fund_maincode(secucode: str):
    """开放式基金存在多类份额或联接基金，其持仓应该查询主基金"""
    mapped = models.FundAssociate.objects.filter(relate=secucode).values('secucode', 'define')
    if not mapped:
        return secucode
    return mapped[0]['secucode']


def asset_type_penetrate(port_code: str, date: datetime.date) -> dict:
    """组合在指定日期的穿透持仓"""
    holdings = models.Holding.objects.filter(port_code=port_code, date=date).values('secucode', 'mkt_cap')
    balance = models.Balance.objects.get(port_code=port_code, date=date)
    net_value = balance.net_asset
    savings = balance.savings
    liquidation = balance.liquidation
    ratio = {x['secucode']: x['mkt_cap'] / net_value for x in holdings}
    ret = {
        'equity': 0, 'fix_income': 0, 'alternative': 0, 'monetary': 0, 'other': 0
    }
    for secucode, allocated in ratio.items():
        allocate = security_asset_type(secucode)
        for item in ret:
            ret[item] += float(allocated) * float(allocate.get(item, 0))
    ret['monetary'] += float((savings + liquidation) / net_value)
    return ret


def portfolio_holding_security(port_code: str, date):
    """组合在给定日期持有的场内证券
    ETF、LOF、股票、债券直接获取比例
    场外公募基金穿透到底层
    """
    holdings = models.Holding.objects.filter(port_code=port_code, date=date).values('secucode', 'mkt_cap')
    balance = models.Balance.objects.get(port_code=port_code, date=date)
    net_value = balance.net_asset
    holdings = {x['secucode']: x['mkt_cap'] / net_value for x in holdings}
    ret = {}
    for secucode, ratio in holdings.items():
        security = models.Security.objects.filter(secucode=secucode).first()
        if not security:
            continue
        # 股票、债券、场内基金
        if security.category_code in ('110503', '110504'):
            ret[secucode] = float(ratio)
        # 场外基金
        elif security.category_code == '110502':
            stocks = fund_holding_stocks(secucode, date)
            stocks = {x: y * float(ratio) for x, y in stocks.items()}
            for stockcode, r in stocks.items():
                if stockcode in ret:
                    ret[stockcode] += r
                else:
                    ret[stockcode] = r
    return ret


def fund_holding_stocks(secucode, date, scale=True):
    """基金持有股票及其占比"""
    maincode = open_fund_maincode(secucode)
    rpt = models.FundHoldingStock.objects.filter(secucode=secucode, date__lte=date).last()
    if rpt is None:
        return {}
    date = rpt.date
    holding = models.FundHoldingStock.objects.filter(secucode=secucode, date=date).values('stockcode', 'ratio')
    sum_ = float(sum(x['ratio'] for x in holding))
    if scale:
        asset = open_fund_asset_type(maincode)
        equity = asset['equity']
    else:
        equity = sum_
    holding = {x['stockcode']: float(x['ratio']) / sum_ * float(equity) for x in holding}
    return holding



