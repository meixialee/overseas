# -*- coding: utf-8 -*-
from scrapy.exceptions import DropItem
import pymongo

class TextPipeline(object): #实现 TextPipeline类用来处理数据
    def __init__(self): #初始化
        self.limit = 20   #设定文章长度限制为20

    #  #下面是判断，当title的长度大于20，大于20的部分抛弃，然后使用...来替代
    def process_item(self, item,spider):
        if len(item['title']):
            if len(item['title']) > self.limit:
                item['title'] = item['title'][0:self.limit].rstrip() + '...'
            return item
        else:
            return DropItem('Missing Title')

class MongoPipeline(object):  #实现 MongoPipeline类用来存入mongoDB
    def __init__(self,mongo_uri,mongo_db):  #初始化mongo_uri,mongo_db
        self.mongo_uri = mongo_uri,
        self.mongo_db = mongo_db

    @classmethod    #代表塔斯一种依赖注入的方式
    def from_crawler (cls,crawler):  #可以用来获取全局配置settings.py里的内容
        return cls(
            mongo_uri= crawler.settings.get('MONGO_URI'),
            mongo_db = crawler.settings.get('MONGO_DB')
        )

    def open_spider(self,spider):  #连接数据库，再连接之前的保证数据库处于开启状态
        self.client = pymongo.MongoClient(self.mongo_uri,port=27017)
        self.db = self.client[self.mongo_db]

    def process_item(self, item,spider): #执行数据插入操作
        name = item.__class__.__name__
        self.db[name].insert(dict(item))
        return item

    def close_spider(self, spider): #关闭数据库
        self.client.close()