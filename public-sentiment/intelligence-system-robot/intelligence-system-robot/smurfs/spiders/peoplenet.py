# -*- coding: utf-8 -*-
# Peoplenet news RSS spider
# @author william
# @version 1.0
import feedparser
import scrapy

from smurfs.item.items import ArticleItem
from smurfs.util.common import url_hash


class PeoplenetSpider(scrapy.Spider):
    """ Peoplenet news RSS spider """
    name = "peoplenet"
    allowed_domains = ["people.com.cn"]
    start_urls = ['http://www.people.com.cn/rss/politics.xml']

    def parse(self, response):
        """ parse the RSS sources """
        source = feedparser.parse(response.url)
        for i in source.get('items'):
            # make article item
            item = ArticleItem()
            item["title"] = i["title"]
            item["url"] = i["link"]
            item["content"] = i["description"]
            item["desc"] = ""  # just be null
            item["pub_date"] = ""  # TODO from news time
            item["hash"] = url_hash(i["link"])

            yield item
