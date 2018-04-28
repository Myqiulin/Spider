# -*- coding: utf-8 -*-
# Page Spider
# @author william
# @version 1.0
import time

from scrapy.selector import Selector

from smurfs.item.items import ArticleItem
from smurfs.spiders.basic import RedisSpider
from smurfs.util.common import url_hash


class PageSpider(RedisSpider):
    """ page spider """
    name = "page"

    def parse(self, response):
        """  """
        selector = Selector(response)
        title = selector.xpath(self.page_config["title_rule"]).extract()[0].encode('utf-8')
        content = selector.xpath(self.page_config["content_rule"]).extract()[0].encode('utf-8')

        # make article item
        item = ArticleItem()
        item["title"] = title
        item["url"] = response.url
        item["content"] = content
        item["pub_date"] = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
        item["hash"] = url_hash(response.url)

        return item
