# encoding: utf-8
"""
@author: cxie
@contact: cxie@ubiquant.com
@time: 2020/9/25 下午4:30
@file: urls.py
@desc: 
"""

from ..tools import to_timestamp

class UrlSummary():

    def list_url(self, market):
        sh_list = 'http://app.finance.ifeng.com/list/stock.php?t=ha&f=symbol&o=asc&p='
        sz_list = 'http://app.finance.ifeng.com/list/stock.php?t=sa&f=chg_pct&o=desc&p='
        if market == 'sh':
            url = sh_list
            return url
        elif market == "sz":
            url = sz_list
            return url
        else:
            raise ValueError('Market do not exist!')

    def price_url(self, stockid, market, start_date, end_date):
        url = 'https://hk.finance.yahoo.com/quote/'
        t0 = str(to_timestamp(start_date))
        t1 = str(to_timestamp(end_date))

        if market =='sh':
            url += str(stockid)+'.SS'+'/history?period1='+t0+'&period2='+t1+'&interval=1d&filter=history&frequency=1d'
            return url
        elif market =='sz':
            url += str(stockid)+'.SZ'+'/history?period1='+t0+'&period2='+t1+'&interval=1d&filter=history&frequency=1d'
            return url
        else:
            raise ValueError('Market do not exist!')

    def industry_url(self, stock, market):
        url='http://vip.stock.finance.sina.com.cn/corp/view/stockIndustryNews.php?symbol=' + market + stock
        return url

    def news_url(self, stock, market):
        url = 'http://vip.stock.finance.sina.com.cn/corp/view/vCB_AllNewsStock.php?symbol=' + market + stock
        return url

    def report_url(self, stock):
        url = 'http://vip.stock.finance.sina.com.cn/corp/view/vCB_AllBulletin.php?stockid='+ stock
        return url

    def comments_url(self, stock, page):
        url_form = 'http://guba.eastmoney.com/list,{},f_{}.html'
        return url_form.format(stock, page)

if __name__ == '__main__':
    us = UrlSummary()
    market = 'sh'
    url = us.list_url(market=market)
