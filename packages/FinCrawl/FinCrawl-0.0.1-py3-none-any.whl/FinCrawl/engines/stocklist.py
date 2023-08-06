# encoding: utf-8
"""
@author: cxie
@contact: cxie@ubiquant.com
@time: 2020/9/25 下午3:28
@file: stocklist.py
@desc: 
"""

from ..urls import UrlSummary

import requests
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np

class clist:

    def crawl(self, url):
        result = pd.DataFrame()
        p = 0

        while p <= 100:
            res=requests.get(url+str(p+1))
            soup = BeautifulSoup(res.text, 'lxml')
            tables = soup.select('body > div.main > div > div.block02 > div > table')
            print("Start Page: ", p)
            try:
                data = tables[0]
            except IndexError:
                print("Crawl Finished")
                return result
            data = pd.read_html(data.prettify())[0]
            stocklist = pd.DataFrame(data.iloc[1:-1,0:2])
            stocklist.columns=['stock', 'name']
            if stocklist.empty:
                print("Crawl Finished")
                return result
            result = pd.concat([result, stocklist], axis=0).reset_index(drop=True)
            p += 1

        return result

    def save(self, result, dir, market):
        result.to_csv(dir+'stocklist_%s.csv'%market, encoding='utf-8', index=False)

if __name__ == '__main__':
    us = UrlSummary()
    market = 'sh'
    c = clist()
    r = c.crawl(url = us.list_url(market))
    dir = '/Users/kylexie/Documents/PycharmProjects/FinancialCrawl/results/'
    c.save(r, dir, market)
