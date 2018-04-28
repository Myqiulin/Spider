# -*- coding: utf-8 -*-
# News Spider
# @author william
# @version 1.0
import json
import time

import scrapy
from scrapy.selector import Selector
from smurfs.util.text_util import TextUtil
from smurfs.item.items import ArticleItem
from smurfs.spiders.basic import RedisSpider
from smurfs.util.common import url_hash


class NewsSpider(RedisSpider):
    """  News spider """
    name = "news"
    util = TextUtil()

    def start_requests(self):
        self.start_time = int(time.time())
        self.url_template = self.settings.get("CONFIG_NEWS_URL_TEMPLATE")
        url = (self.url_template % (self.start_time, self.start_time))
        self.new_base_url = self.settings.get("CONFIG_NEWS_BASE_URL")
        self.default_day = self.settings.getint("CONFIG_NEWS_FETCH_DEFAULT_DAY")
        self.default_time = int(time.time()) - (self.default_day * 24 * 60 * 60)
        self.fetch_time_key = self.settings.get("RDK_NEWS_FETCH_TIME")
        self.last_fetch_time = self.server.get(self.fetch_time_key)
        if self.last_fetch_time is None:
            self.last_fetch_time = self.default_time

        self.comment_url_template = self.settings.get("CONFIG_NEWS_COMMENT_URL")
        self.comment_fetch_number = self.settings.get("CONFIG_NEWS_COMMENT_FETCH_NUMBER")

        yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        """ parse the RSS homepage """
        print "parse the RSS homepage=================="
        json_str = str(response.body)
        if json is None or len(str(json).strip()) == 0:
            return

        resp_json = json.loads(json_str)
        data = resp_json["data"]
        has_next = resp_json["next"]
        max_behot_time = has_next["max_behot_time"]
        next_url = (self.url_template % (max_behot_time, max_behot_time))

        if int(max_behot_time) > int(self.last_fetch_time):
            for item in data:
                if item["title"] is not None:

                    article_genre = item["article_genre"]
                    if article_genre == "article":
                        url = item["source_url"]

                        article_id = item["group_id"]

                        # 链接用于评论
                        print "新闻ID推送————redies=================="
                        self.push_to_comment(article_id)

                        if not str(item["source_url"]).startswith("http"):
                            url = self.new_base_url + item["source_url"]
                        yield scrapy.Request(url=url, callback=self.parse_article,
                                             meta={"title": item["title"], "article_id": article_id})

            self.logger.info("Parse complete, go to the next page.")
            yield scrapy.Request(url=next_url, callback=self.parse)
        else:
            if self.page_config is not None and self.page_config["start_time"] is not None:
                self.start_time = int(self.page_config["start_time"])

            self.last_fetch_time = self.start_time
            self.server.set(self.fetch_time_key, self.last_fetch_time)
            self.logger.info("The fetch job is done, last time is %s.", self.last_fetch_time)
            return

    def push_to_comment(self, article_id):
        page_config = {
            "site_type": "news_comment",
            "url": self.comment_url_template % (article_id, article_id),
            "name": "news_comment"
        }
        self.server.rpush("news_comment:start_urls", json.dumps(page_config))

    def parse_article(self, response):
        """  """
        selector = Selector(response)
        content = selector.xpath("//body/article").extract()
        if content is None or len(content) == 0:
            content = selector.xpath("//div[@class='article-content']").extract()

        if content is None or len(content) == 0:
            return
        # make article item
        article = ArticleItem()
        article["title"] = unicode(response.meta['title'])
        article["id"] = unicode(response.meta['article_id'])
        article["pub_date"] = unicode(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())))
        article["author"] = "NONE"  # TODO 发布者或媒体
        article_html = self.util.format_html(content[0].encode('utf-8'))
        article["content"] = unicode(article_html)
        article_text = self.util.format_text(article_html)
        article["text"] = unicode(article_text)
        article["desc"] = self.util.extract_desc(article_text, 100)
        article["tags"] = self.util.extract_tags(article_text)
        # article["entity"] = ",".join(self.util.extract_entity(article_text))
        article["url"] = response.url
        article["hash"] = url_hash(response.url)
        article["type"] = unicode("新闻")

        return article
