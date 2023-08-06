# encoding: utf-8
"""
@author: cxie
@contact: cxie@ubiquant.com
@time: 2020/9/27 下午1:15
@file: stockprice.py
@desc: 
"""

from ..urls import UrlSummary

import pandas as pd
import numpy as np
from bs4 import BeautifulSoup
import requests

class cprice():

    def crawl(self, url):
        date = []
        price = []
        res = requests.get(url)
        soup = BeautifulSoup(res.text, 'html.parser')
        date.extend([i.string for i in soup.find_all('td',attrs={'class':'Py(10px) Ta(start) Pend(10px)'})])
        price.extend([i.string for i in soup.find_all('td', attrs={'class':'Py(10px) Pstart(10px)'})])

        if len(price) == 0:
            raise ValueError('No Information about this stock!')
        else:
            data=pd.DataFrame(np.array(price).reshape(-1,6),columns=['start','highest','lowest','close','close_adj','volume'])
            data['date']=pd.DataFrame(date, columns=['date'])
            #print("Crawl Finished")
            return data

    def save(self, result, stock, dir):
        result.to_csv(dir+'price/'+'%s.csv'%str(stock), encoding='utf-8', index=False)

if __name__ == '__main__':
    us = UrlSummary()
    stock = '600004'
    market = 'sh'
    url = us.price_url(stock, market, start_date= '2019-05-01', end_date='2019-08-01')
    c = cprice()
    r = c.crawl(url)
    dir = '/Users/kylexie/Documents/PycharmProjects/FinancialCrawl/results/'
    c.save(r, stock, dir)
