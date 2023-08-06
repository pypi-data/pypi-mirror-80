# encoding: utf-8
"""
@author: cxie
@contact: cxie@ubiquant.com
@time: 2020/9/29 下午1:28
@file: setup.py.py
@desc: 
"""

import setuptools

setuptools.setup(
    name="FinCrawl", # Replace with your own username
    version="0.0.1",
    author="Kyle Xie",
    author_email="xiecong@ruc.edu.cn",
    description="A package for crawling financial textual data",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
