# -*- coding: utf-8 -*-
import redis
import json

from smurfs.util.weibo_queue import weibo_queue_list

weibo_api_url = "http://m.weibo.cn/api/container/getIndex"
weibo_home_url = weibo_api_url + "?jumpfrom=weibocom&type=uid&value=%s"
start_urls = list(set(["3213060995","1648726621"]))

client = redis.StrictRedis(host="hadoop002.edcs.org", port=8000, db=0)
for uid in start_urls:
    page_config = {
        "site_type": "weibo",
        "url": weibo_home_url % uid,
        "name": "weibo",
    }
    print uid
    client.rpush(page_config["site_type"] + ":start_urls", json.dumps(page_config))
