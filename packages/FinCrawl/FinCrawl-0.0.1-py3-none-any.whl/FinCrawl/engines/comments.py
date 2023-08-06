# encoding: utf-8
"""
@author: cxie
@contact: cxie@ubiquant.com
@time: 2020/9/28 下午9:43
@file: comments.py
@desc: 
"""

from ..tools import find_change_point
from ..urls import UrlSummary

import pandas as pd
from bs4 import BeautifulSoup

import requests
import re
import datetime
import time

class ccomments():

    def crawl(self, stock, due_date):
        us = UrlSummary()

        page = 1
        current_date = datetime.date.today()
        current_year = current_date.year
        current_date = str(current_date)

        data=pd.DataFrame(columns=['title','read','comment'])
        times = []

        while current_date > due_date:
            url = us.comments_url(stock, page)
            res =requests.get(url)
            res.encoding='utf-8'
            soup = BeautifulSoup(res.text, 'html.parser')
            pinglun = soup.select(".l3 a")
            reads = soup.select(".l1")[1:]
            comments = soup.select(".l2")[1:]
            dates = re.findall("[0-9]{2}-[0-9]{2} [0-9]{2}:[0-9]{2}",str(soup.select('.l5')))

            if len(dates) == 0 or page == 1000:
                print("Information Ended")
                break

            if dates[-1] > dates[0]:
                ind = find_change_point(dates)
                current_year = current_year -1
                for i in range(len(dates)):
                    if i < ind:
                        dates[i] = str(current_year+1)+'-'+dates[i]
                    else:
                        dates[i] = str(current_year)+'-'+dates[i]
            else:
                dates = [str(current_year)+'-'+item for item in dates]

            index=0
            di=0
            while (index+di) < len(pinglun):
                try:
                    pinglun[index+di]['title']
                except KeyError:
                    di=di+1
                    continue
                if pinglun[index+di]['title']=="我提出了一个问题。":
                    di=di+1
                    continue
                data=data.append(pd.DataFrame({'title':[pinglun[index+di]['title']],'read':[reads[index].text],'comment':[comments[index].text]}),ignore_index=True)
                index=index+1

            current_date = dates[-1]
            times.extend(dates)
            page += 1
            time.sleep(2)

        data['date']=pd.DataFrame(times, columns=['date'])
        return data

    def save(self, data, stock, dir):
        data.to_csv(dir+'comments/'+stock+'.csv',index=False, encoding='utf-8')


if __name__ == '__main__':
    stock = '600004'
    due_date = '2020-09-24 00:00'
    c = ccomments()
    r = c.crawl(stock, due_date)
    dir = '/Users/kylexie/Documents/PycharmProjects/FinancialCrawl/results/'
    c.save(r, stock, dir)
