# encoding: utf-8
"""
@author: cxie
@contact: cxie@ubiquant.com
@time: 2020/9/25 下午4:44
@file: CrawlData.py
@desc:  entry point
"""

from .urls import UrlSummary
from .engines import clist, cprice, cindustry, cnews, creport, ccomments

__all__ = ['crawl_list_price', 'crawl_stock_list', 'crawl_stock_price', 'crawl_industry_news',
           'crawl_stock_news', 'crawl_stock_report', 'crawl_stock_comments']

def crawl_stock_list(market, dir):
    us = UrlSummary()
    url = us.list_url(market)
    c = clist()
    r = c.crawl(url = url)
    c.save(r, dir, market)

def crawl_stock_price(stock, market, start_date, end_date, dir):
    us = UrlSummary()
    url = us.price_url(stock, market, start_date, end_date)
    c = cprice()
    r = c.crawl(url)
    c.save(r, stock, dir)

def crawl_industry_news(stock, market, due_date, dir):
    us = UrlSummary()
    url = us.industry_url(stock, market)
    c = cindustry()
    r = c.crawl(url, due_date)
    c.save(r, stock, dir)

def crawl_stock_news(stock, market, due_date, dir):
    us = UrlSummary()
    url = us.news_url(stock, market)
    c = cnews()
    r = c.crawl(url, due_date)
    c.save(r, stock, dir)

def crawl_stock_report(stock, due_date, dir):
    us = UrlSummary()
    url = us.report_url(stock)
    c  = creport()
    r = c.crawl(url, due_date)
    c.save(r, stock, dir)

def crawl_stock_comments(stock, due_date, dir):
    c = ccomments()
    r = c.crawl(stock, due_date)
    c.save(r, stock, dir)

def crawl_list_price(stocklist, market, start_date, end_date, dir):
    errs = []
    for stock in stocklist:
        print("Start Crawling: %s" %stock)
        try:
            crawl_stock_price(stock, market, start_date, end_date, dir)
            print("Finished Crawling: %s"%stock)
        except:
            errs.append(stock)
            print("Error Happens: %s"%stock)
            continue
    print("Finished Stock List, Total Errors: %d"%(int(len(errs))))
    return errs

if __name__ == '__main__':
    dir = '/Users/kylexie/Documents/PycharmProjects/FinancialCrawl/results/'
    mkt = 'sh'
    crawl_stock_list(market=mkt, dir = dir)

    stock = '600004'
    start_date = '2019-05-01 00:00:00'
    end_date = '2019-08-01 00:00:00'
    crawl_stock_price(stock, mkt, start_date, end_date, dir)

    due_date = '2020-09-26'
    crawl_industry_news(stock, mkt, due_date, dir)

    due_date = '2020-01-01'
    crawl_stock_news(stock, mkt, due_date, dir)

    due_date = '2020-01-01'
    crawl_stock_report(stock, due_date, dir)

    due_date = '2020-09-24'
    crawl_stock_comments(stock, due_date, dir)
