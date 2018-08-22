#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Created by qiuyu on 2018/8/8
import pandas as pd
import jieba
from gensim.models import Word2Vec
import numpy as np
from scipy import spatial


def delete_punctuation(text):
    """删除标点符号"""
    #text = re.sub(r'[^0-9A-Za-z\\t]+', 'wo',text)
    text=text.replace(' ','')
    text=text.replace('\n','')
    text=text.replace(' ','')
    text = text.replace('\t', '')
    return text



def avg_feature_vector(sentence, model, vec_size, index2word_set):
    feature_vec = np.zeros((vec_size, ), dtype='float32')
    n_words = 0
    for word in sentence:
        if word in index2word_set:
            n_words += 1
            feature_vec = np.add(feature_vec, model[word])
    if (n_words > 0):
        feature_vec = np.divide(feature_vec, n_words)
    return feature_vec

def remove_like_title():
    vec_size=128
    model_path="/Users/lianqiuyu/Documents/text_classfication/word2vec_model"
    data=pd.read_csv("/Users/lianqiuyu/Documents/image_description_girl_cloth.csv",header=-1)
    data.columns = ['image', 'shopid', 'description', 'title', 'tradeitemid', 'cid0', 'cid1']
    model=Word2Vec.load(model_path)
    index2word_set = set(model.wv.index2word)
    newdata=[]
    for index,iterm in data.iterrows():

        text1 = delete_punctuation(iterm['description'])
        text2 = delete_punctuation(iterm['title'])


        text1 = list(jieba.cut(text1))
        text2 = list(jieba.cut(text2))

        s1_afv = avg_feature_vector(text1, model=model, vec_size=vec_size, index2word_set=index2word_set)
        s2_afv = avg_feature_vector(text2, model=model, vec_size=vec_size,
                                    index2word_set=index2word_set)
        sim = 1 - spatial.distance.cosine(s1_afv, s2_afv)
        #print(sim)
        if sim<0.7:
            tem=[]
            tem.append(iterm['image'])
            tem.append(iterm['shopid'])
            tem.append(delete_punctuation(iterm['description']))
            tem.append(delete_punctuation(iterm['title']))
            tem.append(iterm['tradeitemid'])
            tem.append(iterm['cid0'])
            tem.append(iterm['cid1'])
            #print tem
            newdata.append(tem)
    newdata = pd.DataFrame(newdata)
    newdata.columns = ['image', 'shopid', 'description', 'title', 'tradeitemid', 'cid0', 'cid1']

    newdata.to_csv("/Users/lianqiuyu/Documents/all_sen_smi_get_imag_des.csv",header=True,index=False)
remove_like_title()




