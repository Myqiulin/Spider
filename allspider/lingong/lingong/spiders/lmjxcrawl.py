# -*- coding: utf-8 -*-

import re

import scrapy

from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from scrapy import Request

from lingong.items import LingongItem


class LmjxcrawlSpider(CrawlSpider):
    name = 'lmjxcrawl'
    allowed_domains = ['lmjx.net']
    start_urls = ['https://news.lmjx.net/n_industry.html?p=300']

    rules = (
        Rule(LinkExtractor(allow=r'n_industry\.html\?p='), callback='parse_item', follow=True),
    )

    def parse_item(self, response):

        link_list = response.xpath('//div[@class="item"]/h1/a/@href').extract()
        for link in [ 'https:' + link for link in link_list ]:
            yield Request(link, callback=self.parse_news)

    def parse_news(self,response):
        """处理新闻内容"""
        item = LingongItem()
        item['title'] = response.xpath('//div[@class="article-box"]/h1/text()').extract()[0]
        item['pub_time'] = response.xpath('//div[@class="details-timer left"]/text()').extract()[0].strip()
        try:
            item['content_ori'] = response.xpath('//div[@class="details-author left"]/a[2]/text()').extract()[0]
        except Exception as e:
            item['content_ori'] = '无'
        content =response.xpath('//div[@id="i_art_main"]/content').extract()[0]
        dr = re.compile(r'<[^>]+>', re.S)
        new_content = dr.sub('', content)
        item['content'] = new_content
        yield item
