#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Created by qiuyu on 2018/7/31
import pandas as pd

data=pd.read_csv('/Users/lianqiuyu/Documents/image_description_girl_cloth.csv',header=-1,index_col=-1)
a=[i for i in range(data.shape[0])]
data.index=a
ind=[]
with open("/Users/lianqiuyu/Documents/text_classfication/generate_des.txt",'r') as f:
    for line in f.readlines():
        ind.append(line.strip().split('\t')[0])
newdata=[]
print data.index
for i in ind:
    print i
    #print data.loc[int(i)]
    newdata.append(data.loc[int(i)])
data=pd.DataFrame(newdata)
data.to_csv("/Users/lianqiuyu/Documents/generate_image_description.csv",index=-1,header=-1)



