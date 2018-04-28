# -*- coding: utf-8 -*-

import time
import logging

import pymongo
from hbase import Hbase
from hbase.ttypes import *
from thrift.transport import TSocket
from thrift.transport import TTransport
from scrapy import log

from lingong import settings

class HbasePipeline(object):
    """写入HBase"""
    def __init__(self):
        self.hbase_thrift_server = settings.HBASE_THRIFT_SERVER
        self.hbase_thrift_port = settings.HBASE_THRIFT_PORT
        self.transport = TSocket.TSocket(self.hbase_thrift_server, self.hbase_thrift_port)
        self.transport = TTransport.TBufferedTransport(self.transport)
        protocol = TBinaryProtocol.TBinaryProtocol(self.transport)
        self.client = Hbase.Client(protocol)
        self.transport.open()

    def process_item(self, item, spider):
        try:
            title = item.get("title")
            pub_time = item.get("pub_time")
            content_ori = item.get("content_ori")
            content = item.get("content")
            stamp_time = str(int(time.time()))
            str_time = time.strftime("%Y%m%d%H%M")
            rowkey = '40' + stamp_time + str_time
            w_ttitle = Mutation(column=bytes('info:title'), value=bytes(title))
            wpub_time = Mutation(column=bytes('info:pub_time'), value=bytes(pub_time))
            wcontent_ori = Mutation(column=bytes('info:content_ori'), value=bytes(content_ori))
            w_content = Mutation(column=bytes('info:content'), value=bytes(content))
            self.client.mutateRow('lmjxnews', rowkey, [w_ttitle, wpub_time, wcontent_ori, w_content])

        except Exception as e:
            log.msg(e, level=log.ERROR)

    def spider_closed(self, spider):
        self.transport.close()


class LingongPipeline(object):
    """写入MongoDB"""

    def __init__(self):
        self.mongo_cli = pymongo.MongoClient(host="127.0.0.1", port=27017)
        self.db = self.mongo_cli['lingong']
        self.sheet = self.db['news_data']

    def process_item(self, item, spider):

        self.sheet.insert(dict(item))
        return item
