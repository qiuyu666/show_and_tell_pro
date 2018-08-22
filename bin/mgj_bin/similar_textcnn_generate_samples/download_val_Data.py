#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Created by qiuyu on 2018/7/11

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

    data=pd.read_csv('/home/qiuyu/similar_textcnn_generate_samples/similar_textcnn_samples.csv',skiprows=20000,header=-1)
    image_id=1
    data.columns=['image', 'shopid', 'description', 'title', 'tradeitemid', 'cid0', 'cid1']
    for index,iterm in data.iterrows():
	img_src = 'http://s11.mogucdn.com'+iterm['image']
        #print(img_src)
        s = "%07d" % image_id
        request = urllib2.Request(img_src)
        try:
            response = urllib2.urlopen(request)
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

        urllib.urlretrieve(img_src, image_save_path + image_name + s + '.jpg')
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
        description=iterm['description']
        description=delete_punctuation(description)
        #print(iterm['description'])
        #print(description)
        coco_anno[u'caption'] = description

        coco[u'images'].append(coco_img)
        coco[u'annotations'].append(coco_anno)
        if(image_id%200==0):
            print("image_id=",image_id)
        image_id+=1
    output_file = description_save_path+image_name+'.json'
    with codecs.open(output_file, 'w','utf-8') as fid:
        json.dump(coco, fid, ensure_ascii = False)

    print('Saved to {}'.format(output_file))
process(image_save_path='/home/qiuyu/similar_textcnn_generate_samples/val_data/',
       image_name='similar_textcnn_val_',description_save_path='/home/qiuyu/similar_textcnn_generate_samples/')
#process(image_save_path='/home/qiuyu/textcnn_generate_data/train_data/',
       # image_name='generate_train_',description_save_path='/home/qiuyu/textcnn_generate_data')
