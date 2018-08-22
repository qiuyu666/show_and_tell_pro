#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Created by qiuyu on 2018/7/24
import scrapy
from scrapy import signals
import sys
reload(sys)
sys.setdefaultencoding("utf-8")
import os
from selenium import webdriver
import time

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
import urllib
import random
import os


class XhscrawlerItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pfilename = scrapy.Field()
    subUrls = scrapy.Field()
    head = scrapy.Field()
    content = scrapy.Field()



class XhscrawlerPipeline(object):
    def process_item(self, item, spider):
        head = (item['head'])
        filename = head + ".txt"
        #当文章已爬取过,不再重复保存
        if not os.path.exists(item['pfilename'] + '/' + filename):
            fp = open(item['pfilename'] + '/' + filename, 'w')
            fp.write(item['content'])
            fp.close()
        return item


class XiaohsSpider(scrapy.Spider):
    name = 'xiaohs'
#    allowed_domains = ['xiaohongshu.com']
#    start_urls = ['http://xiaohongshu.com/']
    def __init__(self, searchfile = './searchfile.txt'):
        '''
        :param searchfile.txt 格式：
         小个子:小个子,小个子穿搭,矮个子...
         微胖:微胖,微胖穿搭...
         A型:A型身材,梨形身材穿搭...
         （半角冒号和逗号）
        '''
        super(XiaohsSpider, self).__init__()
        searchwords = []   #存放全部搜索词
        searchwordsDict = dict()   #区分搜索词所属体型描述词
        with open(searchfile, 'r') as sfile:
            for line in sfile:
                key = line.strip('\n').strip().split(':')[0]
                values = (line.strip('\n').split(':')[1]).split(',')
                searchwords.extend(values)
                searchwordsDict[key] = values
        dcap = dict(DesiredCapabilities.PHANTOMJS)
        dcap["phantomjs.page.settings.userAgent"] = (
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_3) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.54 Safari/536.5")
        self.searchwords = searchwords
        self.searchwordsDict = searchwordsDict
        self.allowed_domains = ['xiaohongshu.com']
        self.start_urls = ['http://www.xiaohongshu.com/search_result/%s' % sw for sw in searchwords]
        self.driver = webdriver.PhantomJS(desired_capabilities=dcap)
        self.driver.set_page_load_timeout(5)



def parse(self, response):
    items = []
    #指定存储路径
    sw = (response.url.split('search_result/'))[1]
    #unquote转utf-8
    sw_u = urllib.unquote(sw).decode('utf-8')
    skey = ''
    for key in self.searchwordsDict.keys():
        if sw_u in self.searchwordsDict[key]:
            skey = key
            break
    if skey == '':
        print "something wrong happened in searchwordsDict!!!"
    filename = './data/%s' % skey
    #如果目录不存在，则创建目录
    if(not os.path.exists(filename)):
        os.makedirs(filename)
    self.driver.get(response.url)
    #暂停2-4秒
    time.sleep(2 + random.random() * 2)
    subUrls = []
    try:
        #elelist = self.driver.find_elements_by_xpath('//div[@class="note-list-box"]//a')
        #subUrls = [ele.get_attribute('href') for ele in elelist]
        #print '\n'.join(subUrls)
        for i in range(2):    #点击2次显示更多,显示60条
            try:
                more = self.driver.find_element_by_xpath('//div[@class="note-list-box"]/div[@class="more"]/span')
                more.click()
            except Exception as ee:
                print ee
                break
            time.sleep(0.5)
        elelist = self.driver.find_elements_by_xpath('//div[@class="note-list-box"]//a')
        subUrls = [ele.get_attribute('href') for ele in elelist]
        #print len(subUrls)
    except Exception as e:
        print e
    #爬取所有子页面url
    for i in range(len(subUrls)):
        item = XhscrawlerItem()
        item['pfilename'] = filename
        item['subUrls'] = subUrls[i]
        items.append(item)
    #加载每个子页面,发送子页面url的Request请求，得到Response后连同包含meta数据 一同交给回调函数 detail_parse 方法处理
    for item in items:
        yield scrapy.Request(url=item['subUrls'], meta={'meta_1':item}, callback = self.detail_parse)


#获取文章标题和内容
    def detail_parse(self, response):
        item = response.meta['meta_1']
        heads = response.xpath('//div[@class="left-card"]//h3[@class="title"]/text()').extract()
        content_list = response.xpath('//div[@class="left-card"]//div[@class="content"]/p/text()').extract()
        if len(heads) == 0:
            if len(content_list) == 0:
                head = "notitleandcontent"
                print item['subUrls'] + ' has no title and content!!!!'
            else:
                head = content_list[0].replace(' ','')
        else:
            head = heads[0].replace(' ','')
        content = '\n'.join(content_list)
        item['head'] = head
        item['content'] = content
        yield item