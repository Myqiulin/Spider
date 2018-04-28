# -*- coding: utf-8 -*-

import sys
reload(sys)
sys.setdefaultencoding('utf-8')

import scrapy

from lingong.pipelines import LingongPipeline

class LmjxSpider(scrapy.Spider):
    name = "LMJX"
    allowed_domains = ["lmjx.net"]
    start_urls = ['https://news.lmjx.net/n_industry.html']

    def parse(self, response):
        item = LingongPipeline()
        a_list = response.xpath('//div[@class="item"]/h1/a/@href').extract()
        for url in a_list:
            url = "http:" + url
            yield scrapy.Request(url=url,callback=self.parse_title)


    def parse_title(self,response):
        content_detail = response.xpath('//content/p/text()').extract()[0]
        print content_detail
