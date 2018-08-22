#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Created by qiuyu on 2018/8/20


from __future__ import print_function
import os
import json
import time
import random
from PIL import Image
import pandas as pd
import urllib2
import urllib
from socket import timeout as socket_timeout
import codecs
import sys
import re



reload(sys)
sys.setdefaultencoding('utf8')


def delete_punctuation(text):
    """删除标点符号"""
    #text = re.sub(r'[^0-9A-Za-z\\t]+', 'wo',text)
    text=text.replace(' ','')
    text=text.replace('\n','')
    text=text.replace(' ','')
    text = text.replace('\t', '')
    return text





def process(image_save_path,description_save_path,image_name):
    coco = dict()
    coco[u'info'] = {u'desciption': u'MGJ tradeitem image description in mscoco format'}
    coco[u'licenses'] = ['Unknown', 'Unknown']
    coco[u'images'] = list()
    coco[u'annotations'] = list()

    data=pd.read_csv('/Users/lianqiuyu/Downloads/qiuyu_get_zhuye_look_comments.csv',skiprows=52000,header=-1)
    image_id=1
    data.columns=['image','comment']
    ima_comments={}
    for index,iterm in data.iterrows():
        if iterm['image'] not in ima_comments.keys():
            ima_comments.setdefault(iterm['image'], []).append(iterm['comment'])
        else:
            ima_comments[iterm['image']].append(iterm['comment'])
    for key in ima_comments.keys():
        if len(ima_comments[key])>1:
            print (len(ima_comments[key]))
        if key.split(':')[0]=='http':
            img_src = key
        else:
            try:
                img_src = 'http://s11.mogucdn.com' + key
            except:
                print("imageurl type error")
                continue
        #print(img_src)
        s = "%07d" % image_id
        request = urllib2.Request(img_src)
        try:
            response = urllib2.urlopen(request)
            urllib.urlretrieve(img_src, image_save_path + image_name + s + '.jpg')
        except urllib2.HTTPError as e:
            print(e)
            continue
        except socket_timeout:
            print("连接超时了，休息一下...")
            time.sleep(random.randint(15, 25))
            continue
        except urllib2.URLError:
            print("url error")
            continue
        except urllib.ContentTooShortError:
            print("urllib.ContentTooShortError")
            continue


        img = Image.open(image_save_path + image_name + s + '.jpg')
        width, height = img.size
        coco_img = {}
        coco_img[u'license'] = 0
        coco_img[u'file_name'] = image_name + s + '.jpg'
        coco_img[u'width'] = width
        coco_img[u'height'] = height
        coco_img[u'date_captured'] = 0
        coco_img[u'coco_url'] = img_src
        coco_img[u'flickr_url'] = img_src
        coco_img['id'] = image_id

        coco_anno = {}
        coco_anno[u'image_id'] = image_id
        coco_anno[u'id'] = image_id
        caps=[]
        for description in ima_comments[key]:
            description=delete_punctuation(description)
            caps.append(description)
        #print(iterm['description'])
        #print(description)
        coco_anno[u'caption'] = caps

        coco[u'images'].append(coco_img)
        coco[u'annotations'].append(coco_anno)
        if(image_id%200==0):
            print("image_id=",image_id)
        image_id+=1
    output_file = description_save_path+image_name+'.json'
    with codecs.open(output_file, 'w','utf-8') as fid:
        json.dump(coco, fid, ensure_ascii = False)

    print('Saved to {}'.format(output_file))
#process(image_save_path='/Users/lianqiuyu/Documents/image_description/val_data/',
#       image_name='mgj_val_',description_save_path='/Users/lianqiuyu/Documents/image_description/')
process(image_save_path='/Users/lianqiuyu/Documents/comment_test/zhuye_look_images/',image_name='zhuye_look_comment_test',description_save_path='/Users/lianqiuyu/Documents/comment_test/')