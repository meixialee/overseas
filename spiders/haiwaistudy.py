# !/usr/bin/env python
# -*- coding: utf-8 -*-
import scrapy
from ..items import HaiwaiwangItem

class HaiwaiSpider(scrapy.Spider):
    name = 'haiwaistudy'   #爬虫名
    allowed_domains = ['theory.haiwainet.cn']  #爬虫域
    start_urls = ['http://theory.haiwainet.cn/study/']  #爬虫开始url

    def parse(self, response):    #-parse（）方法的参数 resposne 是 start_urls 里面的链接爬取后的结果。
        items = response.xpath('//div[@class="w650 show_list fl"]/ul/li')
        for im in items:
            item = HaiwaiwangItem()
            item['title'] = im.xpath('./a/text()').extract()
            item['link'] = im.xpath('./a/@href').extract()
            yield item

        for i in range(2,7):   #循环2到六页链接
            url = "http://theory.haiwainet.cn/study/" +str(i) + ".html" #构造链接请求
            #  #使用scrapy.Request请求下一页的url并使用回调函数把交给上面的 parse（）方法进行解析
            yield scrapy.Request(url=url,callback=self.parse)

