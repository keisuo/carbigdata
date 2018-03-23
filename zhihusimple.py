# coding=utf-8
# !/usr/bin/python

import requests
from bs4 import BeautifulSoup
from xlutils.copy import copy
import xlrd
import time
import json

headers={"User-Agent":"Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.140 Safari/537.36"}

count =0
rb = xlrd.open_workbook(r'./data/car.xls')
wb = copy(rb)
sh = wb.get_sheet(0)
r = requests.get("https://www.zhihu.com/topic/20033948/top-answers",headers=headers)
bs = BeautifulSoup(r.content.decode("utf-8"),"html.parser")
data = bs.find_all('div',{'class':'List-item TopicFeedItem'})

for idata in data:
    content1 = idata.find('meta',{'itemprop':'name'})['content']
    print(content1)
    try:
        content2 = idata.find('meta',{'itemprop':'upvoteCount'})['content']
    except:
        content2 = idata.find('button', {'class': 'Button LikeButton ContentItem-action'}).text
    print(content2)
    try:
        content3 = idata.find('span',{'class','UserLink AuthorInfo-name'}).find('a',{'class':'UserLink-link'}).text
    except:
        content3 = '匿名用户'
    print(content3)

    try:
        content4 = idata.find('div',{'class':'AuthorInfo-badgeText'}).text
    except AttributeError:
        content4 = ''
    print(content4)
    content5 = idata.find('meta', {'itemprop':'commentCount'})['content']
    print(content5)

    urls = idata.find_all('meta', {'itemprop':'url'})
    content6 = ''
    zhuanlan = 0
    for url in urls:
        if 'answer' in url['content']:
            content6 = url['content']
            break
        elif 'zhuanlan' in url['content']:
            zhuanlan = 1
            content6 = url['content'].replace('//','/')
            break

    print('url',content6)
    t_s=BeautifulSoup(requests.get(content6, headers=headers).content.decode("utf-8"), "html.parser")
    if zhuanlan ==0:
        content7=t_s.find('span', {'itemprop': 'text','class':'RichText CopyrightRichText-richText'}).get_text()
    else:
        content7 = t_s.find('div', {'class': 'RichText PostIndex-content av-paddingSide av-card'}).get_text()

    print(content7)

    sh.write(count,0,content1)
    sh.write(count,1,content2)
    sh.write(count,2,content3)
    sh.write(count,3,content4)
    sh.write(count,4,content5)
    sh.write(count,5,content6)
    sh.write(count,6,content7)
    count+=1
wb.save(r'./data/car.xls')