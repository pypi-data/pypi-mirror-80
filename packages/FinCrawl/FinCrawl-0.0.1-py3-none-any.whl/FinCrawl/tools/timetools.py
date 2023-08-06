# encoding: utf-8
"""
@author: cxie
@contact: cxie@ubiquant.com
@time: 2020/9/27 下午1:10
@file: timetools.py
@desc: 
"""

import time

__all__ = ['to_timestamp', 'find_change_point']

def to_timestamp(timestr):
    t = time.strptime(timestr, '%Y-%m-%d %H:%M:%S')
    t = int(time.mktime(t))
    return t


def find_change_point(arr):
    for index, item in enumerate(arr):
        if index == 0:
            continue
        elif item > arr[index-1]:
            return index
