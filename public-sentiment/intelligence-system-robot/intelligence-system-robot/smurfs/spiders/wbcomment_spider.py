# -*- coding: utf-8 -*-
import json
import urlparse

import requests
from scrapy.http import Request

from smurfs.item.items import CommentItem
from smurfs.spiders.basic import RedisSpider
from smurfs.util.common import parse_time
from smurfs.util.text_util import TextUtil
from smurfs.util.emotions_util import EmotionsUtil


class WBCommentSpider(RedisSpider):
    name = "wb_comment"
    # redis_key = "wb_comment"
    # https://m.weibo.cn/single/rcList?format=cards&id=%s&type=comment&hot=1
    util = TextUtil()
    e_util = EmotionsUtil();
    com_info_url = "http://m.weibo.cn/api/container/getIndex?containerid=%s_-_INFO&type=uid&value=%s"

    def parse_json(self, response):
        item = None
        try:
            json_str = response.body
            item = dict(json.loads(json_str))
            if int(item.get("ok")) != 1:
                self.logger.error(
                    "result is failed: %s,url: %s." % (json.dumps(dict(item), ensure_ascii=False), response.url))
        except Exception, e:
            self.logger.error("parse response error: %s, response: %s" % (e, response.body))
        return item

    def parse(self, response):
        json_str = response.body
        item = json.loads(json_str)
        if item.get("max") is None:
            return
        maxpage = int(str(item.get("max")))
        # 取出前10页
        maxpage = maxpage > 100 and 100 or maxpage
        if maxpage != 0:
            for i in range(2, maxpage + 1):
                url = response.url + "&page=%s" % i
                # 解析URL参数
                info_id = self.process_url(url, 'id')
                print "url===================%s" % url
                yield Request(url=url, callback=self.parse_comments, meta={"info_id": info_id})

    def process_url(self, url, key):

        """解析url参数"""
        url_parse = urlparse.urlparse(url)
        params = urlparse.parse_qs(url_parse.query, True)
        return params[key][0]

    # 解释每一页的热评
    def parse_comments(self, response):
        print "*****************进入hot解析 url:%s" % response.url
        json_str = response.body
        item = json.loads(json_str)
        comments = item.get("data").strip()
        wbcommentitem = CommentItem()
        if comments:
            for comment in comments:
                if comment.get("text") is None or len(comment.get("text").strip()) <= 0:
                    continue
                create_time = comment.get("created_at")
                text = comment.get("text")
                com_text = self.util.format_text(text)
                com_text = self.process_text(com_text)
                com_content = self.util.format_html(text)

                like_counts = comment.get("like_counts")
                userinfo = comment.get("user")
                com_user_id = userinfo.get("id")
                wbcommentitem['info_id'] = response.meta['info_id']
                wbcommentitem['com_id'] = comment.get("id")
                wbcommentitem['com_time'] = unicode(parse_time(create_time))
                wbcommentitem['com_username'] = userinfo.get("screen_name")
                wbcommentitem['com_userinfo'] = userinfo
                wbcommentitem['com_userid'] = com_user_id
                wbcommentitem['com_liked'] = like_counts
                wbcommentitem['com_text'] = com_text
                wbcommentitem['com_content'] = com_content
                wbcommentitem['com_source'] = "微博".encode('utf-8')

                wbcommentitem['com_sentiments'] = self.e_util.extract_sentiments(com_text.decode("utf-8"))
                wbcommentitem['com_tags'] = self.util.extract_tags(com_text)

                url = "http://m.weibo.cn/api/container/getIndex?jumpfrom=weibocom&type=uid&value=%s"
                # yield wbcommentitem
                yield Request(url=url % com_user_id, meta={"item": wbcommentitem, }, callback=self.parse_user,
                              dont_filter=False)

    # 解析内容："回复@用户:内容"
    def process_text(self, text):
        if text == '' or text is None:
            return text
        if '@' in text and ':' in text:
            text = text[text.find('@'):][text[text.find('@'):].find(':') + 1:]
        return text

    # # 解释每一页的热评
    # def parse_hot(self, response):
    #     print "进入hot解析"
    #     print "解析的url:%s" % response.url
    #     json_str = response.body
    #     item = dict(json.loads(json_str)[0])
    #     print "item长度%s" % len(item)
    #     groups = item.get("card_group")
    #     wbcommentitem = CommentItem()
    #     for comment in groups:
    #         if comment:
    #             create_time = dict(comment).get("created_at")
    #             text = dict(comment).get("text")
    #             html_text = self.util.format_text(text)
    #             like_counts = dict(comment).get("like_counts")
    #             userinfo = comment.get("user")
    #             useritems = dict(json.loads(userinfo))
    #             com_user_id = useritems.get("id")
    #             wbcommentitem['info_id'] = comment.get("id")
    #             wbcommentitem['com_time'] = unicode(parse_time(create_time))
    #             wbcommentitem['com_username'] = useritems.get("screen_name")
    #             wbcommentitem['com_userinfo'] = userinfo
    #             wbcommentitem['com_userid'] = com_user_id
    #             wbcommentitem['com_liked'] = like_counts
    #             wbcommentitem['com_text'] = text
    #             wbcommentitem['com_content'] = html_text
    #             wbcommentitem['com_source'] = "微博".encode('utf-8')
    #             url = "http://m.weibo.cn/api/container/getIndex?jumpfrom=weibocom&type=uid&value=%s"
    #             yield wbcommentitem
    #             yield Request(url=url % com_user_id, meta={"item": wbcommentitem, }, callback=self.parse_user,
    #                           dont_filter=False)

    def parse_user(self, response):
        """ 解析用户个人信息 """
        item = self.parse_json(response)
        if item is None:
            return
        tabsinfo = item.get("tabsInfo")
        if tabsinfo is None:
            self.logger.error("tabsInfo is None,url: %s." % response.url)
            return
        tabs = tabsinfo.get("tabs")
        userInfo = item.get("userInfo")
        wbcommentitem = response.meta['item']
        uid = userInfo.get("id")
        home_id = None
        weibo_id = None
        for tab in tabs:
            if isinstance(tab, dict) and tab.get("title") and tab.get("title") == "主页":
                home_id = tab["containerid"]
            if isinstance(tab, dict) and tab.get("title") and tab.get("title") == "微博":
                weibo_id = tab["containerid"]

        if home_id is None or weibo_id is None:
            self.logger.warning("home_id or weibo_id is null,Retrying to request... %s", response.url)
            yield Request(url=response.url, callback=self.parse)
        info_url = self.com_info_url % (home_id, uid)
        rep = requests.get(info_url, cookies=response.request.cookies, timeout=5)
        if rep.status_code != 200:
            self.logger.error("Response status is failed: %s,url: %s." % (rep.status_code, rep))
            return
        item = dict(json.loads(rep.content))
        cards = item.get("cards")
        if cards is None:
            self.logger.error("cards is None,url: %s." % response.url)
            return
        for card in cards:
            card_group = card.get("card_group")
            if card_group:
                for g in card_group:
                    if g.has_key("item_name"):
                        item_name = g.get("item_name")
                        if item_name == "所在地":
                            location = str(g.get("item_content")).split(" ")
                            if len(location) > 1:
                                # personItem["province"] = location[0].decode("utf-8")
                                wbcommentitem['com_location'] = location[1].decode("utf-8")
                            else:
                                # personItem["province"] = g.get("item_content")
                                wbcommentitem['com_location'] = g.get("item_content")

        yield wbcommentitem
