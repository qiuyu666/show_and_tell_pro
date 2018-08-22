#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Created by qiuyu on 2018/7/26
import jieba
import jieba.analyse
import pandas as pd
import logging
import os
import gensim

# jieba.load_userdict('userdict.txt')
# 创建停用词list
def stopwordslist(filepath):
    stopwords = [line.strip() for line in open(filepath, 'r', encoding='utf-8').readlines()]
    return stopwords


# 对句子进行分词
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


def any2unicode(text, encoding='utf8', errors='strict'):
    """Convert a string (bytestring in `encoding` or unicode), to unicode."""
    if isinstance(text, unicode):
        return text
    return unicode(text, encoding, errors=errors)


def fenci(input_fpath,out_fpath):
    data=pd.read_csv(input_fpath,header=-1)
    data.columns=['image','shopid','description','title','tradeitemid','cid0','cid1']
    sentences = []
    for index,iterm in data.iterrows():
        text=delete_punctuation(iterm['description'])
        #print text
        #text=seg_sentence(text)
        text=list(jieba.cut(text))
        sentences.append(text)


        text = delete_punctuation(iterm['title'])
        #print text
        #text=seg_sentence(text)
        #text = list(jieba.cut(iterm['title']))
        text = list(jieba.cut(text))
        sentences.append(text)
    #print sentences

    #sentences=sentences.encode('utf-8')
    logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)


    model = gensim.models.Word2Vec(sentences, size=128, window=4, min_count=3, negative=3,
                             sample=0.001, hs=1, workers=4)
    # for key in model.wv.vocab.keys():
    #     print key
    # print model[u"的"]
    print model.wv.similarity(u"夏季", u"新款")
    #model.wv.save_word2vec_format(out_fpath)
    model.save("/Users/lianqiuyu/Documents/text_classfication/word2vec_model")



fenci(input_fpath='/Users/lianqiuyu/Documents/image_description_girl_cloth.csv',out_fpath='/Users/lianqiuyu/Documents/text_classfication/word2vector_1.txt')
