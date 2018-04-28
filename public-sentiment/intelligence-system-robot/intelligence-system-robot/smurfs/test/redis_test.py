# -*- coding: utf-8 -*-
import json
import redis
import time

# page
# page_config = {
#     "site_type": "page",
#     "url": "http://news.qq.com/a/20170423/019787.htm",
#     "name": "tenxun",
#     "title_rule": "/html/head/title/text()",
#     "content_rule": "//div[@id='Cnt-Main-Article-QQ']",
# }

# news
now_time = str(int(time.time()))
page_config = {
    "site_type": "news",
    "url": "http://www.toutiao.com/api/pc/feed/?category=__all__&utm_source=toutiao&widen=1&max_behot_time=" + now_time + "&max_behot_time_tmp=" + now_time,
    "name": "toutiao",
    "start_time": now_time
}

client = redis.StrictRedis(host="hadoop002.edcs.org", port=8000, db=0)
# client.lpush(page_config["site_type"] + ":start_urls", json.dumps(page_config))

# cursor = -1
# count = 10
# lists = []
#
# while cursor != 0:
#     if cursor == -1:
#         cursor = 0
#     (cursor, sets) = client.scan(cursor=cursor, match="weibo:cookies:*", count=count)
#     for s in sets:
#         lists.append(s)
#
# print lists

print "weibo:cookies:123343rfwddddddddddddddddddddddef"[14:]