#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Created by qiuyu on 2018/7/26
import pandas as pd
import jieba
import json

def seg_sentence(sentence):
    sentence = list(jieba.cut(sentence.strip()))
    stopwords = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't',
                 'u', 'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N',
                 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z', '1', '2', '3', '4', '5', '6', '7', '8',
                 '9', '0']  # 这里加载停用词的路径 # 这里加载停用词的路径
    sentence = [w for w in sentence if w not in stopwords]

    return sentence
def delete_punctuation(text):
    """删除标点符号"""
    #text = re.sub(r'[^0-9A-Za-z\\t]+', 'wo',text)
    text=text.replace(' ','')
    text=text.replace('\n','')
    text=text.replace(' ','')
    text = text.replace('\t', '')
    return text

#data=pd.read_csv('/Users/lianqiuyu/Documents/text_classfication/des_title.csv',header=-1,skiprows=20000)
data=pd.read_csv('/Users/lianqiuyu/Documents/image_description_girl_cloth.csv',header=-1)
#data.columns=['description','title']
data.columns=['image','shopid','description','title','tradeitemid','cid0','cid1']
#with open('/Users/lianqiuyu/Documents/text_classfication/test1.txt','w') as f:
with open('/Users/lianqiuyu/Documents/text_classfication/selet_description.txt','w') as f:
    line3=''
    for index,iterm in data.iterrows():
        line1 = delete_punctuation(iterm['description'])
        #text = seg_sentence(text)
        #line=''
        #for w in text:
            #line+=' '+w
        #print line1
        f.write(line1)
        f.write('\t'+'1'+'\n')

        # line2 = delete_punctuation(iterm['title'])
        # # text = seg_sentence(text)
        # #line = ''
        # # for w in text:
        # #     line += ' ' + w
        # #line2 = line2 + '\t' + '0'+'\n'
        # f.write(line2)
        # f.write('\t' + '0' + '\n')
    f.write("春季新款长裙")
    f.write('\t' + '0' + '\n')
f.close()

# with open('/Users/lianqiuyu/Documents/text_classfication/ydic.txt','w') as f:
#     f.write("20")
#     f.write("\n")
#
#     line={"0":0,"1":1}
#     f.writelines(str(line) + "\n")
# f.close()



