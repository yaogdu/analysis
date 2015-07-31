# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

from pymongo import MongoClient


import logging as log


class MongoDBPipeline(object):
    def __init__(self):
        self.server = '192.168.100.186'
        self.port = 20301
        self.db = 'weixin'
        self.col = 'article'
        #connection = pymongo.Connection(self.server,self.port)
        connection = MongoClient(self.server,self.port)
        db = connection[self.db]
        self.collection = db[self.col]

    def save(self, item):
        
        self.collection.insert(dict(item))
        
        return item
