#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Created by qiuyu on 2018/8/7
import pandas as pd
def delete_punctuation(text):
    """删除标点符号"""
    #text = re.sub(r'[^0-9A-Za-z\\t]+', 'wo',text)
    text=text.replace(' ','')
    text=text.replace('\n','')
    text=text.replace(' ','')
    text = text.replace('\t', '')
    return text

#data=pd.read_csv('/Users/lianqiuyu/Documents/text_classfication/des_title.csv',header=-1,skiprows=20000)
# data=pd.read_csv('/Users/lianqiuyu/Documents/get_pos_sample.csv',header=-1)
# data.columns=['description']
# with open('/Users/lianqiuyu/Documents/train_data.txt','w') as f:
#     for index,iterm in data.iterrows():
#         line1 = delete_punctuation(iterm['description'])
#         f.write(line1)
#         f.write('\t'+'1'+'\n')
# data=pd.read_csv('/Users/lianqiuyu/Documents/get_neg_sample.csv',header=-1)
# data.columns=['title']
# with open('/Users/lianqiuyu/Documents/train_data.txt','a') as f:
#     for index,iterm in data.iterrows():
#         line1 = delete_punctuation(iterm['title'])
#         f.write(line1)
#         f.write('\t'+'0'+'\n')

data=pd.read_csv('/Users/lianqiuyu/Documents/get_neg_sample.csv',header=-1,nrows=10000)
data.columns=['title']
with open('/Users/lianqiuyu/Documents/text_classfication/test_all_neg.txt','w') as f:
    line1 = "这款穿上真的很仙女哦～"
    f.write(line1)
    f.write('\t' + '1' + '\n')
    for index,iterm in data.iterrows():
        line1 = delete_punctuation(iterm['title'])
        f.write(line1)
        f.write('\t'+'0'+'\n')
