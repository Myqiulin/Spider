# -*- coding: utf-8 -*-
# Weibo Spider
# @author william
# @version 1.0
import json
import requests
from scrapy.http import Request

from smurfs.item.items import PersonItem, TweetsItem, RelationshipsItem
from smurfs.spiders.basic import RedisSpider
from smurfs.util.common import parse_time
from smurfs.util.text_util import TextUtil
from smurfs.util.weibo_queue import weibo_queue_list


class WeiboSpider(RedisSpider):
    name = "weibo"
    util = TextUtil()

    weibo_url = "http://m.weibo.cn"
    # redis_key = "SinaSpider:start_urls"
    start_urls = list(set(weibo_queue_list))

    weibo_api_url = "http://m.weibo.cn/api/container/getIndex"
    weibo_home_url = weibo_api_url + "?jumpfrom=weibocom&type=uid&value=%s"
    weibo_info_url = weibo_api_url + "?containerid=%s_-_INFO&type=uid&value=%s"
    weibo_follower_url = weibo_api_url + "?containerid=%s&type=uid&value=%s"
    weibo_follower_next_url = weibo_follower_url + "&page=%s"
    weibo_content_url = weibo_api_url + "?type=uid&value=%s&containerid=%s"
    weibo_cnt_next_url = weibo_content_url + "&page=%s"
    weibo_comment_url = "https://m.weibo.cn/single/rcList?format=cards&id=%s&type=comment&hot=1"
    wb_comment_url = "https://m.weibo.cn/api/comments/show?id=%s"
    def_follower = "231051_-_followers_-_%s"
    def_fans = "231051_-_fans_-_%s"

    # 此段不需要，保留测试
    def start_requests(self):
        for uid in self.start_urls:
            yield Request(url=self.weibo_home_url % uid, callback=self.parse)

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

        personItem = PersonItem()
        uid = userInfo.get("id")
        personItem["uid"] = uid
        personItem["follow_count"] = userInfo.get("follow_count")
        personItem["fans_count"] = userInfo.get("followers_count")
        personItem["nikename"] = userInfo.get("screen_name")
        nikename = userInfo.get("screen_name")
        personItem["tweets_count"] = userInfo.get("statuses_count")
        personItem["verified"] = userInfo.get("verified")
        personItem["verified_reason"] = userInfo.get("verified_reason")

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

        info_url = self.weibo_info_url % (home_id, uid)

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
                        if item_name == "标签":
                            personItem["tags"] = g.get("item_content")
                        if item_name == "性别":
                            personItem["gender"] = g.get("item_content")
                        if item_name == "所在地":
                            location = str(g.get("item_content")).split(" ")
                            if len(location) > 1:
                                personItem["province"] = location[0].decode("utf-8")
                                personItem["city"] = location[1].decode("utf-8")
                            else:
                                personItem["province"] = g.get("item_content")
                                personItem["city"] = g.get("item_content")
                        if item_name == "简介":
                            personItem["description"] = g.get("item_content")
                        if item_name == "学校":
                            personItem["school"] = g.get("item_content")
                        if item_name == "邮箱":
                            personItem["email"] = g.get("item_content")
                        if item_name == "等级":
                            personItem["level"] = g.get("item_content")
                        if item_name == "阳光信用":
                            personItem["sunshine_credit"] = g.get("item_content")
                        if item_name == "注册时间":
                            personItem["registration"] = g.get("item_content")
                        if item_name == "公司":
                            personItem["company"] = g.get("item_content")
                        if item_name == "博客":
                            personItem["blog"] = g.get("item_content")
        yield personItem
        yield Request(url=self.weibo_content_url % (uid, weibo_id),
                      callback=self.parse_person_tweets,
                      dont_filter=False,
                      meta={"_uid": uid, "_home_id": home_id, "_weibo_id": weibo_id, "_unm": nikename})

        follower_id = self.def_follower % uid
        fans_id = self.def_fans % uid
        yield Request(url=self.weibo_follower_url % (follower_id, uid),
                      callback=self.parse_follower,
                      dont_filter=False,
                      meta={"_uid": uid, "_c_id": follower_id})
        yield Request(url=self.weibo_follower_url % (fans_id, uid),
                      callback=self.parse_follower,
                      dont_filter=True,
                      meta={"_uid": uid, "_c_id": fans_id})

    def parse_person_tweets(self, response):
        """ 解析用户所有微博 """
        item = self.parse_json(response)
        if item is None:
            return

        cardlistInfo = item.get("cardlistInfo")
        # total_tweets = cardlistInfo.get("total")
        page_index = cardlistInfo.get("page")
        if page_index is None or page_index == "null":
            return

        uid = response.meta['_uid']
        home_id = response.meta['_home_id']
        weibo_id = response.meta['_weibo_id']
        nikename = response.meta['_unm']

        cards = item.get("cards")
        for card in cards:
            mblog = card.get("mblog")
            if mblog:
                tweets = TweetsItem()
                created_at = str(mblog.get("created_at"))  # 创建时间
                tweets["create_time"] = unicode(parse_time(created_at))

                text = mblog.get("text").decode("unicode_escape")
                article_text = self.util.format_text(text)
                tweets_html = self.util.format_html(text)
                tweets["content"] = tweets_html
                tweets["text"] = article_text
                tweets["tags"] = self.util.extract_tags(article_text)

                tweets["source"] = mblog.get("source")  # 发布来源（手机）
                tweets["comments_count"] = mblog.get("comments_count")  # 评论次数
                tweets["attitudes_count"] = mblog.get("attitudes_count")  # 赞次数
                tweets["reposts_count"] = mblog.get("reposts_count")  # 转发次数
                tweets["uid"] = mblog.get("user").get("id")  # 用户ID
                tweets["id"] = mblog.get("id")  # 内容ID
                tweets["bid"] = mblog.get("bid")  # 微博ID
                tweets["title"] = unicode("%s的微博" % nikename)
                page_info = mblog.get("page_info")  # 位置 page_title
                if page_info:
                    tweets["location"] = mblog.get("page_info").get("page_title")
                # 链接用于评论
                print "微博ID推送redis=================="
                self.push_to_comment(mblog.get("id"))
                yield tweets

        yield Request(url=self.weibo_cnt_next_url % (uid, weibo_id, page_index),
                      callback=self.parse_person_tweets,
                      dont_filter=False,
                      meta={"_uid": uid, "_home_id": home_id, "_weibo_id": weibo_id, "_unm": nikename})

    def push_to_comment(self, uid):
        page_config = {
            "site_type": "wb_comment",
            "url": self.wb_comment_url % uid,
            "name": "wb_comment",
        }
        self.server.rpush("wb_comment:start_urls", json.dumps(page_config))

    def push_to_queue(self, uid):
        page_config = {
            "site_type": self.name,
            "url": self.weibo_home_url % uid,
            "name": self.name,
        }
        self.server.rpush(self.name + ":start_urls", json.dumps(page_config))

    def parse_follower(self, response):
        """  解析用户关注与粉丝关系 """
        item = self.parse_json(response)
        if item is None:
            return

        uid = response.meta['_uid']
        _c_id = response.meta['_c_id']

        cardlistInfo = item.get("cardlistInfo")
        # total_tweets = cardlistInfo.get("total")
        page_index = cardlistInfo.get("page")
        if page_index is None or page_index == "null":
            return

        try:
            cards = item.get("cards")
            for card in cards:
                card_group = card.get("card_group")
                for g in card_group:
                    if g and g.get("user"):
                        relationship = RelationshipsItem()
                        relationship["follower"] = uid
                        relationship["be_follower"] = g.get("user").get("id")
                        # 将微博写入Redis队列
                        print "# 将微博写入Redis队列"
                        self.push_to_queue(g.get("user").get("id"))
                        # yield relationship
        except Exception, e:
            self.logger.error(
                "parse relationship item error: %s, data:%s." % (e, json.dumps(dict(item), ensure_ascii=False)))

        yield Request(url=self.weibo_follower_next_url % (_c_id, uid, page_index),
                      callback=self.parse_follower,
                      dont_filter=False,
                      meta={"_uid": uid, "_c_id": _c_id})
