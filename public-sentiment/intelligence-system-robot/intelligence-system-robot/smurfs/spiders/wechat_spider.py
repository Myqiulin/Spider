# -*- coding: utf-8 -*-
# Wechat Spider
# @author william
# @version 1.0
from bs4 import BeautifulSoup
from scrapy.http import Request
from scrapy.selector import Selector

from smurfs.item.items import WechatUserItem, ArticleItem
from smurfs.spiders.basic import RedisSpider
from smurfs.util.common import url_hash
from smurfs.util.text_util import TextUtil
from smurfs.util.wechat_queue import wechat_queue_list


class WechatSpider(RedisSpider):
    """ wechat spider """
    name = "wechat"

    start_queue = list(set(wechat_queue_list))

    search_api_url = "http://weixin.sogou.com/weixin"
    search_url = search_api_url + "?type=1&s_from=input&query=%s&ie=utf8&_sug_=n"
    article_url = search_api_url + "?type=2&query=%s&tsn=3&from=tool"
    util = TextUtil()

    def start_requests(self):
        for wid in self.start_queue:
            yield Request(url=self.search_url % wid, callback=self.parse, dont_filter=False)

    def parse(self, response):
        """  """
        selector = Selector(response)
        item = selector.xpath("//ul[@class='news-list2']/li").extract()

        for i in item:
            soup = BeautifulSoup(str(i), "lxml")
            user = WechatUserItem()

            user["nikename"] = unicode(str(soup.find(attrs={"class": "tit"}).get_text()).replace("\n", ""))
            wid = str(soup.find(attrs={"name": "em_weixinhao"}).get_text()).replace("\n", "")
            user["wid"] = unicode(wid)
            user["profile_url"] = unicode(soup.find(attrs={"class": "tit"}).find("a").get('href'))
            dd_arr = soup.find_all("dd")
            if len(dd_arr) == 3:
                user["description"] = dd_arr[0].get_text()
                user["authentication"] = dd_arr[1].get_text()

            yield user
            yield Request(url=self.article_url % wid, callback=self.parse_article_item, dont_filter=False, meta={"_uname": user["nikename"]})
        # parse next page
        next_page_url = selector.xpath("//a[@id='sogou_next']/@href").extract()
        if next_page_url is None or len(next_page_url) == 0:
            return
        yield Request(url=self.search_api_url + next_page_url[0], callback=self.parse, dont_filter=False)

    def parse_article_item(self, response):
        selector = Selector(response)
        item = selector.xpath("//ul[@class='news-list']/li").extract()
        uname = response.meta['_uname']

        for i in item:
            soup = BeautifulSoup(str(i), "lxml")
            publish_user = soup.find(attrs={"class": "account"}).get_text()
            if publish_user == uname:
                # title = str(soup.find("h3").get_text()).replace("\n", "")
                article_url = soup.find("h3").find("a").get('href')
                yield Request(url=article_url, callback=self.parse_article_content, dont_filter=False, meta={"_uname": uname})
        # parse next page
        next_page_url = selector.xpath("//a[@id='sogou_next']/@href").extract()
        if next_page_url is None or len(next_page_url) == 0:
            return
        yield Request(url=self.search_api_url + next_page_url[0], callback=self.parse_article_item, dont_filter=False, meta={"_uname": uname})

    def parse_article_content(self, response):
        selector = Selector(response)

        article_name = selector.xpath("//h2[@id='activity-name']/text()").extract()[0].encode("utf-8")
        if article_name:
            article_name = str(article_name).replace("\r", "").replace("\n", "").strip()
        article_author = response.meta['_uname']
        article_date = unicode(selector.xpath("//em[@id='post-date']/text()").extract()[0].encode("utf-8"))
        article_content = selector.xpath("//div[@id='js_content']").extract()[0].encode('utf-8')

        article = ArticleItem()
        article["title"] = unicode(article_name)
        article["pub_date"] = unicode(article_date)
        article["author"] = article_author
        article_html = self.util.format_html(article_content)
        article["content"] = unicode(article_html)
        article_text = self.util.format_text(article_html)
        article["text"] = unicode(article_text)
        article["desc"] = self.util.extract_desc(article_text, 100)
        article["tags"] = self.util.extract_tags(article_text)
        article["entity"] = ",".join(self.util.extract_entity(article_text))
        article["url"] = response.url
        article["hash"] = url_hash(response.url)
        article["type"] = unicode("微信公众号")
        yield article
