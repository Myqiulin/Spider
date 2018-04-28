# -*- coding: utf-8 -*-
import redis
import json

from smurfs.util.weibo_queue import weibo_queue_list

search_api_url = "http://weixin.sogou.com/weixin"
search_url = search_api_url + "?type=1&s_from=input&query=%s&ie=utf8&_sug_=n"
start_urls = list(set(["旅游", "岛", "生活", "师生", "专栏"]))

client = redis.StrictRedis(host="hadoop002.edcs.org", port=8000, db=0)
for keyword in start_urls:
    page_config = {
        "site_type": "wechat",
        "url": search_url % keyword,
        "name": "wechat",
    }
    print keyword
    client.rpush(page_config["site_type"] + ":start_urls", json.dumps(page_config))
