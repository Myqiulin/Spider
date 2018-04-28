# -*- coding: utf-8 -*-
import scrapy
from scrapy import Request
import jsonpath, json
import re

class WeiboSpider(scrapy.Spider):
    name = "weibo"
    allowed_domains = ['weibo.cn']
    # 综合
    n = 0
    # cps_url = "https://m.weibo.cn/api/container/getIndex?containerid=100103type=1%26q=山东临工&featurecode=20000320&lfid=106003type=1&luicode=10000011&oid=4103996270375689&queryVal=山东临工&title=山东临工&type=all&page={}"
    cps_url = "https://m.weibo.cn/api/container/getIndex?containerid=100103type=60%26q=山东临工%26t=0&lfid=106003type=1&luicode=10000011&queryVal=山东临工&title=山东临工&type=all&page="
    start_urls = [cps_url + str(n)]

    def parse(self, response):

        # 实时
        time_url = "https://m.weibo.cn/api/container/getIndex?containerid=100103type=61%26q=山东临工%26t=0&featurecode" \
                   "=20000320&lfid=100103type=60%26q=山东临工%26t=0&luicode=10000011&page=4&queryVal=山东临工&title=山东临工&type=all"

        # 热门
        hot_url = "https://m.weibo.cn/api/container/getIndex?containerid=100103type=60%26q=山东临工%26t=0&featurecode" \
                  "=20000320&lfid=100103type=61%26q=山东临工%26t=0&luicode 10000011&queryVal=山东临工&title=山东临工&type=all"

        # 文章
        aricle_url = "https://m.weibo.cn/api/container/getIndex?containerid=100103type=21%26q=山东临工%26t=0&featurecode" \
                     "=20000320&lfid=100103type=60%26q=山东临工%26t=0&luicode=10000011&queryVal=山东临工&title=山东临工&type=all"

        json_content = json.loads(response.text)
        text_list = jsonpath.jsonpath(json_content, '$..ok')
        # card_list = jsonpath.jsonpath(json_content, '$.data.cards.card_group[*]')
        card_list = jsonpath.jsonpath(json_content, '$..card_group[*]..mblog..idstr')
        if card_list:
            for idstr in card_list:
                blog_url = "https://m.weibo.cn/statuses/extend?id={}".format(idstr)
                yield Request(blog_url, meta={'idstr':idstr}, callback=self.parse_blog)
        # print text_list
        self.n += 1
        url = self.cps_url + str(self.n)
        if str(text_list[0]) != str(0):
            yield Request(url, callback=self.parse)

    def parse_blog(self, response):
        """处理每条博客,获取全文"""
        json_content = json.loads(response.text)
        # 获取到点击全文按钮后的全部博文内容
        blog = jsonpath.jsonpath(json_content, '$..longTextContent').pop()
        html_pattern = re.compile(r'<[^>]+>', re.S)
        result = html_pattern.sub('', blog)
        # print(result)
        idstr = response.meta['idstr']
        offset = 1
        comment_url = "https://m.weibo.cn/api/comments/show?id={0}&page={1}"
        yield Request(comment_url.format(idstr, offset),
                      meta={'idstr':idstr, 'comment_url':comment_url, 'offset':offset},
                      callback=self.parse_comment)

    def parse_comment(self, response):
        """处理评论"""
        idstr = response.meta['idstr']
        offset = response.meta['offset']
        comment_url = response.meta['comment_url']
        offset+=1
        json_content = json.loads(response.text)
        flag = jsonpath.jsonpath(json_content, '$..ok').pop()
        if str(flag) == '1':
            text_list = jsonpath.jsonpath(json_content, '$.data.data..text')
            print text_list.pop()
            yield Request(comment_url.format(idstr, offset),
                          meta={'idstr':idstr, 'comment_url':comment_url, 'offset':offset},
                          callback=self.parse_comment)

