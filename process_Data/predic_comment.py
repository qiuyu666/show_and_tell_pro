#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Created by qiuyu on 2018/8/10
import pandas as pd
import json
import urllib

#预测是否为广告评论
def predict_is_adcomment(sentence):
    pre_url = 'http://crm.algo.meili-inc.com/http/proxy/group/neuron-pre/api/' \
              'query.htm?app=demo&scene=deep_text_categorization&sentence='+sentence
    request = urllib.urlopen(pre_url)
    response = request.read()
    #print response
    responseJSON = json.loads(response)
    return responseJSON['response']['10.50.220.146:8118']['response']['predicted']['prediction']


#预测是否为差评
def predict_is_badcomment(sentence):
    pre_url = 'http://crm.algo.meili-inc.com/http/proxy/group/neuron-pre/api/' \
              'query.htm?app=demo&scene=deep_emotion_categorization&sentence=' + sentence
    request = urllib.urlopen(pre_url)
    response = request.read()
    #print response
    responseJSON = json.loads(response)
    return responseJSON['response']['10.50.220.146:8118']['response']['predicted']['prediction']



def predict_allcomments(file_path,out_path):
    data=pd.read_csv(file_path,header=-1)
    data.columns=['objectid','content','cover']
    #过滤差评
    print "filter bad comments"
    new_data=[]
    for index,iterm in data.iterrows():
        comment=iterm['content']
        try:
            re=predict_is_badcomment(comment)
        except:
            print 'urlerror'
            continue
        if re==2:
            new_data.append(data.ix[index])
    new_data=pd.DataFrame(new_data)

    new_data.columns = ['objectid','content','cover']

    #过滤广告评论
    print "filter ads"
    result_data=[]
    for index,iterm in new_data.iterrows():
        comment=iterm['content']
        try:
            re=predict_is_adcomment(comment)
        except:
            print 'urlerror'
            continue
        if re==1:
            result_data.append(new_data.ix[index])
    print "finish filter"
    result_data=pd.DataFrame(result_data)
    result_data.to_csv(out_path,header=False,index=False)
predict_allcomments(file_path='/Users/lianqiuyu/Documents/qiuyu_get_comments_v2.csv',
                    out_path='/Users/lianqiuyu/Documents/filtered_comments_v2.csv')
