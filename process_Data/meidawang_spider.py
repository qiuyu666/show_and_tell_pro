#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Created by qiuyu on 2018/7/24
from bs4 import BeautifulSoup
import requests
import codecs
import re
import pandas as pd


def download_page(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_2) '
                      'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.80 Safari/537.36'
    }
    data = requests.get(url, headers=headers).content
    return data

def parse_article():
    title = []
    zhaiyao=[]
    content_list=[]
    image = []
    for i in range(1,22):
        if i==1:
            url="http://www.zzmmgo.com/dress/index.html"
            html = download_page(url)
        else:
            url="http://www.zzmmgo.com/dress/"+str(i)+".html"
            html = download_page(url)
        soup = BeautifulSoup(html, 'html.parser')
        # 从上面的数据获取html文档并解析，这里使用的是Python自带的HTML解释器

        for article in soup.find_all('div', attrs={'class': 'fashion_list_img fl'}):

            # 缩小HTML文档的解析范围，限定在文章主体内部。
            content = article.find('a')
            title.append(content['title'])
            # 获取文章主体内部的<h1>标签内的文本，可以发现这就是标题内容。
            link_src=content['href']
            link_html = download_page(link_src)
            link_soup=BeautifulSoup(link_html, 'html.parser')
            link_zhaiyao=link_soup.find('div', attrs={'class': 'fashion_left_zhaiyao'})
            if link_zhaiyao:
                print link_zhaiyao.get_text()
                link_zhaiyao=link_zhaiyao.get_text()

            link_content = link_soup.find('div', attrs={'class': 'fashion_left_content'})
            if link_content.find('p'):
                link_content=link_content.find('p').getText()
                #print link_content
            content_list.append(link_content)
            zhaiyao.append(link_zhaiyao)

            link_images=[]
            link_images.append(content.find('img')['src'])
            for img_link in link_soup.find_all('p', attrs={'style': 'text-align: center;'}):
                if img_link.find('img'):
                    link_images.append(img_link.find('img')['src'])
            if len(link_images)==1:
                for img_link in link_soup.find_all('div', attrs={'style': 'text-align: center;'}):
                    if img_link.find('img'):
                        link_images.append(img_link.find('img')['src'])
                if len(link_images)==1:
                    print "no more pictures"
            image.append(link_images)
            #image.append(content.find('img')['src'])
        i+=1
    print len(title)
    print len(image)
    title=pd.Series(title)
    zhaiyao=pd.Series(zhaiyao)
    content_list=pd.Series(content_list)
    image=pd.Series(image)
    data=pd.concat([title,zhaiyao,content_list,image],axis=1)
    print data
    data.columns=['title','zhaiyao','content','images']
    data.to_csv("/Users/lianqiuyu/Documents/meidawang.csv",header=-1,encoding='utf_8_sig')


parse_article()





