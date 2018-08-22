#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Created by qiuyu on 2018/7/11
from __future__ import print_function
import os
import argparse
import json
from PIL import Image

def convert2coco(args):
    dataset = json.load(open(args.caption_json, 'r'))
    imgdir = args.img_dir

    coco = dict()
    coco[u'info'] = { u'desciption':u'AI challenger image caption in mscoco format'}
    coco[u'licenses'] = ['Unknown', 'Unknown']
    coco[u'images'] = list()
    coco[u'annotations'] = list()

    for ind, sample in enumerate(dataset):
        img = Image.open(os.path.join(imgdir, sample['image_id']))
        width, height = img.size

        coco_img = {}
        coco_img[u'license'] = 0
        coco_img[u'file_name'] = sample['image_id']
        coco_img[u'width'] = width
        coco_img[u'height'] = height
        coco_img[u'date_captured'] = 0
        coco_img[u'coco_url'] = sample['url']
        coco_img[u'flickr_url'] = sample['url']
        coco_img['id'] = ind

        coco_anno = {}
        coco_anno[u'image_id'] = ind
        coco_anno[u'id'] = ind
        coco_anno[u'caption'] = sample['caption']

        coco[u'images'].append(coco_img)
        coco[u'annotations'].append(coco_anno)

        print('{}/{}'.format(ind, len(dataset)))

    output_file = os.path.join(os.path.dirname(args.caption_json), 'coco_'+os.path.basename(args.caption_json))
    with open(output_file, 'w') as fid:
        json.dump(coco, fid)
    print('Saved to {}'.format(output_file))


def main(args):
    convert2coco(args)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Convert AI challenger image caption annotations to mscoco format')
    parser.add_argument('--caption_json', default='ai_challenger_caption_train_20170902/caption_train_annotations_20170902.json', type=str, help='caption json file path')
    parser.add_argument('--img_dir', default='ai_challenger_caption_train_20170902/caption_train_images_20170902', type=str, help='description')
    args = parser.parse_args()
    print(args)
    main(args)
