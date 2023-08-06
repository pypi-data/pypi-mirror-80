# encoding: utf-8
"""
@author: cxie
@contact: cxie@ubiquant.com
@time: 2020/9/27 下午3:34
@file: news.py
@desc: 
"""

from ..urls import UrlSummary

import pandas as pd
from bs4 import BeautifulSoup
import requests
import re
import datetime

class cnews():

    def crawl(self, url, due_date):
        page = 1
        times=[]
        titles=[]
        now_date = str(datetime.date.today())

        while now_date >= due_date:
            res=requests.get(url+'&Page=%d'%page)
            res.encoding='gbk'
            soup=BeautifulSoup(res.text,'html.parser')
            datelist = soup.find_all('div',attrs={'class':'datelist'})
            if len(datelist) == 0 or page == 100:
                print("Information Ended")
                break
            else:
                dates = re.findall("\xa0([0-9]{4}-[0-9]{2}-[0-9]{2})\xa0", str(datelist[0]))
                times.extend(dates)
                now_date = min(times)
                tmps = datelist[0].find_all('a',attrs={'target':'_blank'})
                for tmp in tmps:
                    titles.append(tmp.string)
            page += 1

        data = pd.DataFrame({'time':times, 'title':titles}, columns=['time', 'title'])
        return data

    def save(self, data, stock, dir):
        data.to_csv(dir+'news/'+stock+'.csv',index=False, encoding='utf-8')

if __name__ == '__main__':
    us = UrlSummary()
    stock = '600004'
    market = 'sh'
    url = us.industry_url(stock, market)
    due_date = '2020-01-01'
    c = cindustry()
    r = c.crawl(url, due_date)
    dir = '/Users/kylexie/Documents/PycharmProjects/FinancialCrawl/results/'
    c.save(r, stock, dir)
