#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Created by qiuyu on 2018/8/13
import pandas as pd


Data=pd.read_csv('/Users/lianqiuyu/Documents/filtered_comments_v2.csv',header=-1)
print Data.shape
Data.columns=['id','cover', 'comment']
cov_askey={}
com_askey={}
for index,iterm in Data.iterrows():
    if iterm['cover'] not in cov_askey.keys():
        cov_askey[iterm['cover']]=1
    else:
        cov_askey[iterm['cover']] += 1

    if iterm['comment'] not in com_askey.keys():
        com_askey.setdefault(iterm['comment'],[]).append(iterm['cover'])
    else:
        com_askey.setdefault(iterm['comment'], []).append(iterm['cover'])
comment_res=[]
for key in com_askey.keys():
    tem=[]
    tem.append(str(key))
    tem.append(str(com_askey[key][0]))
    comment_res.append(tem)
    #print cov[key]
res_data=pd.DataFrame(comment_res)
res_data.to_csv('/Users/lianqiuyu/Documents/uniq_comments_samples_v2.csv',header=False,index=False)

print 'coveras_key 共有',len(cov_askey.keys()),'条内容'
print 'commentas_key 共有',len(com_askey.keys()),'条内容'