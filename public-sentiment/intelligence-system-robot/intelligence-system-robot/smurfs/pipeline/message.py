# -*- coding: utf-8 -*-
# Elasticsearch pipeline
# @author william
# @version 1.0
import time

from elasticsearch import Elasticsearch
from scrapy.exceptions import NotConfigured

from smurfs.item.items import ArticleItem, TweetsItem
from smurfs.util.text_util import TextUtil


class ElasticsearchPipeline(object):
    """ Elasticsearch pipeline """

    def __init__(self, es_server, es_username, es_password, es_index, es_type, ):
        self.es_server = es_server
        self.es_username = es_username
        self.es_password = es_password
        self.es_index = es_index
        self.es_type = es_type

        self.server = Elasticsearch(str(self.es_server).split(","))

    @classmethod
    def from_crawler(cls, crawler):
        if not crawler.settings.getbool('ELASTICSEARCH_PIPELINE_ENABLED'):
            raise NotConfigured

        return cls(
            es_server=crawler.settings.get("ELASTICSEARCH_SERVER"),
            es_username=crawler.settings.get("ELASTICSEARCH_USERNAME"),
            es_password=crawler.settings.get("ELASTICSEARCH_PASSWORD"),
            es_index=crawler.settings.get("ELASTICSEARCH_INDEX"),
            es_type=crawler.settings.get("ELASTICSEARCH_TYPE"),
        )

    def open_spider(self, spider):
        print 'into ElasticsearchPipeline.'

    def close_spider(self, spider):
        print 'close ElasticsearchPipeline...'

    def process_item(self, item, spider):
        if not isinstance(item, ArticleItem) and not isinstance(item, TweetsItem):
            return item

        if isinstance(item, ArticleItem):
            self.insert_article(item)
        if isinstance(item, TweetsItem):
            self.insert_tweets(item)

        return item

    def insert_article(self, item):
        if item.get("text") and len(item.get("text")) > 0:
            self.server.index(
                index=self.es_index,
                doc_type=self.es_type,
                id=int(item["hash"]),
                body={
                    "infoTitle": item.get("title"),
                    "infoSrc": item.get("url"),
                    "infoType": item.get("type"),
                    "infoContent": item.get("content"),
                    "infoText": item.get("text"),
                    "infoDesc": item.get("desc"),
                    "infoDate": item.get("pub_date"),
                    "infoTag": item.get("tags"),
                    "infoEntity": item.get("entity"),
                    "infoAuthor": item.get("author"),
                    "timestamp": long(int(round(time.time() * 1000)))
                }
            )

    def insert_tweets(self, item):
        textutil = TextUtil()
        text = textutil.format_text(item.get("text"))
        desc = textutil.extract_desc(text, 10)
        tags = textutil.extract_tags(text)
        entity = ",".join(textutil.extract_entity(text))

        self.server.index(
            index=self.es_index,
            doc_type=self.es_type,
            id=int(item["id"]),
            body={
                "infoTitle": item.get("title"),
                "infoSrc": ("http://m.weibo.cn/u/%s" % item["uid"]),
                "infoType": "微博".decode("utf-8"),
                "infoContent": item.get("text"),
                "infoText": text.decode("utf-8"),
                "infoDesc": desc.decode("utf-8"),
                "infoDate": item.get("create_time"),
                "infoTag": tags.decode("utf-8"),
                "infoEntity": entity.decode("utf-8"),
                "timestamp": long(int(round(time.time() * 1000)))
            }
        )
