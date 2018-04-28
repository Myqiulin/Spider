# -*- coding: utf-8 -*-
import json
import urlparse

from scrapy.http import Request

from smurfs.item.items import CommentItem
from smurfs.spiders.basic import RedisSpider
from smurfs.util.common import parse_time_stamp
from smurfs.util.text_util import TextUtil
from smurfs.util.emotions_util import EmotionsUtil


class NewsCommentSpider(RedisSpider):
    name = "news_comment"
    # redis_key = "news_comment"
    # https://m.weibo.cn/single/rcList?format=cards&id=%s&type=comment&hot=1
    util = TextUtil()
    e_util = EmotionsUtil()
    # com_info_url = "http://m.weibo.cn/api/container/getIndex?containerid=%s_-_INFO&type=uid&value=%s"

    def parse(self, response):

        json_str = response.body
        data_str = json.loads(json_str).get("data")
        total = data_str.get("total")  # 拿到热点评论的总数
        url = response.url

        self.check_response(response)
        # 解析URL参数
        group_id = self.process_url(url)

        print "url===================%s" % url
        yield Request(url=url + "&count=%s" % total, callback=self.parse_comments, meta={"group_id": group_id})

    def check_response(self, response):

        json_str = response.body
        data_str = json.loads(json_str).get("data")
        try:
            if int(data_str.get("message")) != 'success':
                self.logger.error(
                    "result is failed: %s,url: %s." % (data_str, response.url))
        except Exception, e:
            self.logger.error("parse response error: %s, response: %s" % (e, response.body))
        pass

    def process_url(self, url):

        """解析url参数"""
        url_parse = urlparse.urlparse(url)
        params = urlparse.parse_qs(url_parse.query, True)
        return params['group_id'][0]

    # 解析内容："内容 //@用户:..."
    def process_text(self, text):
        if '//@' in text:
            text = text.split("//@")[0]
        return text
    # 解释评论
    def parse_comments(self, response):
        print "进入comments解析***"
        print "解析的url:%s" % response.url
        comment_reply_url = self.settings.get("CONFIG_NEWS_COMMENT_REPLY_URL")
        # 校验返回参数
        self.check_response(response)
        json_str = response.body
        data_str = json.loads(json_str).get("data")
        comments = data_str.get("comments")
        comment_item = CommentItem()
        # 文章ID
        article_id = response.meta['group_id']
        if comments:
            for comment in comments:
                if comment.get("text") is None or len(comment.get("text").strip()) <= 0:
                    continue
                create_time = comment.get("create_time")
                text = comment.get("text")
                com_text = self.util.format_text(text)
                com_text = self.process_text(com_text)
                com_html = self.util.format_html(text)
                digg_count = comment.get("digg_count")
                userinfo = comment.get("user")
                com_user_id = userinfo.get("user_id")
                comment_item['info_id'] = article_id
                comment_item['com_id'] = comment.get("id")
                comment_item['com_time'] = unicode(parse_time_stamp(create_time))
                comment_item['com_username'] = userinfo.get("screen_name")
                comment_item['com_userinfo'] = userinfo
                comment_item['com_userid'] = com_user_id
                comment_item['com_liked'] = digg_count
                comment_item['com_text'] = com_text
                comment_item['com_content'] = com_html
                comment_item['com_location'] = ''
                comment_item['com_source'] = '新闻'.encode('utf-8')
                comment_item['com_sentiments'] = self.e_util.extract_sentiments(com_text.decode("utf-8"))
                comment_item['com_tags'] = self.util.extract_tags(com_text)
                yield comment_item

                reply_count = comment.get("reply_count")
                dongtai_id = comment.get("dongtai_id")
                comment_id = comment.get("id")
                # url = self.settings.get("CONFIG_NEWS_COMMENT_REPLY_URL")

                yield Request(url=comment_reply_url % (comment_id, dongtai_id, reply_count),
                              callback=self.parse_reply, meta={"group_id": article_id})

    # 解释评论的回复
    def parse_reply(self, response):
        print "进入comments_reply解析****"
        print "解析的url:%s" % response.url
        # 校验返回参数
        self.check_response(response)
        json_str = response.body
        data_str = json.loads(json_str).get("data")
        comments = data_str.get("data")
        # 文章ID
        article_id = response.meta['group_id']
        comment_item = CommentItem()
        if comments:
            for comment in comments:
                if comment.get("text") is None or len(comment.get("text").strip()) <= 0:
                    continue
                create_time = comment.get("create_time")
                text = self.process_text(comment.get("text"))
                com_html = self.util.format_html(text)
                com_text = self.util.format_text(text)
                digg_count = comment.get("digg_count")
                userinfo = comment.get("user")
                # useritems = dict(json.loads(userinfo))
                com_user_id = userinfo.get("user_id")
                comment_item['info_id'] = article_id
                comment_item['com_id'] = comment.get("id")
                comment_item['com_time'] = unicode(parse_time_stamp(create_time))
                comment_item['com_username'] = userinfo.get("screen_name")
                comment_item['com_userinfo'] = userinfo
                comment_item['com_userid'] = com_user_id
                comment_item['com_liked'] = digg_count
                comment_item['com_text'] = com_text
                comment_item['com_content'] = com_html
                comment_item['com_location'] = ''
                comment_item['com_source'] = '新闻'.encode('utf-8')
                comment_item['com_sentiments'] = self.e_util.extract_sentiments(com_text.decode("utf-8"))
                comment_item['com_tags'] = self.util.extract_tags(com_text)
                yield comment_item
