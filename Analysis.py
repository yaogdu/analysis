#!/usr/bin/python
# -*- coding: utf-8 -*-
import os
import re
import time
import json
import scrapy
import urllib
import urllib2
import urlparse
import random

from proxy import PROXIES
from agents import AGENTS

import logging as log
from scrapy.selector import HtmlXPathSelector
#from itemss import item
#from gzhArticle.settings import BIZ_FILE
#from gzhArticle.settings import KEY_FILE
from pyquery import PyQuery as pq
from flask import Flask,request
from flask.ext import restful
from db import MongoDBPipeline
app = Flask(__name__)
api = restful.Api(app)

class Analysis(restful.Resource):
    
# 请求前需转义 &  为 %26    
#curl -i http://127.0.0.1:5000/a -d "key=http://mp.weixin.qq.com/s?__biz=MjM5NzMzODM5Ng==&mid=207718447&idx=1&sn=5c22a71643b09c65d6c05176895c1814&3rd=MzA3MDU4NTYzMw==&scene=6#rd" -X PUT
   def put(self,url):
        print 'bbb'
        key = request.form['key']

        proxy = eval(json.dumps(random.choice(PROXIES)))['ip_port']
        
        req = urllib2.Request(key)
        req.add_header('User-Agent',random.choice(AGENTS))
        #req.meta['proxy'] = proxy
        req.proxy=proxy
        response = urllib2.urlopen(req)
        d=pq(response.read())
        item = {}
        item['title'] = d('title').text()
        item['datetime'] = d('#post-date').text()
        item['author']=d('#post-user').text()
        item['contenturl']=key
        #item['tinyurl']='tinyurl'
        item['digest']=d('.rich_media_content>p').find('span').text()
        md = MongoDBPipeline()
        md.save(item)
        return item  
         
#定义restful接口及参数
api.add_resource(Analysis, '/<string:url>')

if __name__ == '__main__':
    app.run(debug=True)
    
 

 
  



