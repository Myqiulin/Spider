# -*- coding: utf-8 -*-
import time

import redis
from scrapy import signals
from scrapy.exceptions import NotConfigured

from smurfs.item.items import ArticleItem, TweetsItem


class SpiderMetrics(object):
    def __init__(self, redis_host, redis_port, redis_encoding, metrics_key_daily_inrc, metrics_key_types_inrc):
        self.items_scraped = 0
        self.redis_host = redis_host
        self.redis_port = redis_port
        self.redis_encoding = redis_encoding
        self.metrics_key_daily_inrc = metrics_key_daily_inrc
        self.metrics_key_types_inrc = metrics_key_types_inrc

        self.server = redis.StrictRedis(host=redis_host, port=redis_port, encoding=redis_encoding, db=0)

    @classmethod
    def from_crawler(cls, crawler):
        # first check if the extension should be enabled and raise
        # NotConfigured otherwise
        if not crawler.settings.getbool('METRICS_ENABLED'):
            raise NotConfigured

        redis_host = crawler.settings.get("REDIS_HOST")
        redis_port = crawler.settings.get("REDIS_PORT")
        redis_encoding = crawler.settings.get("REDIS_ENCODING")
        metrics_key_daily_inrc = str(crawler.settings.get("RDK_METRICS_DAILY_INRC"))
        metrics_key_types_inrc = str(crawler.settings.get("RDK_METRICS_TYPES_INRC"))

        # instantiate the extension object
        ext = cls(redis_host=redis_host,
                  redis_port=redis_port,
                  redis_encoding=redis_encoding,
                  metrics_key_daily_inrc=metrics_key_daily_inrc,
                  metrics_key_types_inrc=metrics_key_types_inrc
                  )
        # connect the extension object to signals
        crawler.signals.connect(ext.spider_opened, signal=signals.spider_opened)
        crawler.signals.connect(ext.spider_closed, signal=signals.spider_closed)
        crawler.signals.connect(ext.item_scraped, signal=signals.item_scraped)
        # return the extension object
        return ext

    def spider_opened(self, spider):
        spider.log("opened spider %s" % spider.name)

    def spider_closed(self, spider):
        spider.log("closed spider %s" % spider.name)

    def statistic_daily_incr(self, item):
        info_type = None
        if isinstance(item, ArticleItem):
            if str(item.get("type")) == "微信公众号":
                info_type = "WECHAT"
            if str(item.get("type")) == "新闻":
                info_type = "NEWS"
        if isinstance(item, TweetsItem):
            info_type = "WEIBO"

        if info_type:
            today = time.strftime('%Y%m%d', time.localtime(time.time()))
            redis_key = self.metrics_key_daily_inrc + today
            result = self.server.get(redis_key)
            if result:
                self.server.set(redis_key, int(result) + 1)
            else:
                self.server.set(redis_key, 1)

    def statistic_types_incr(self, item):
        result = self.server.hgetall(self.metrics_key_types_inrc)
        maps = {}
        if result:
            maps = dict(result)

        info_type = None
        if isinstance(item, ArticleItem):
            if str(item.get("type")) == "微信公众号":
                info_type = "WECHAT"
            if str(item.get("type")) == "新闻":
                info_type = "NEWS"
        if isinstance(item, TweetsItem):
            info_type = "WEIBO"

        if info_type:
            if maps.get(info_type):
                num = int(maps.get(info_type)) + 1
                self.server.hset(self.metrics_key_types_inrc, info_type, num)
            else:
                self.server.hset(self.metrics_key_types_inrc, info_type, 1)

    def item_scraped(self, item, spider):
        self.items_scraped += 1
        # statistics
        self.statistic_daily_incr(item)
        self.statistic_types_incr(item)
