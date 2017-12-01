# -*- coding: utf-8 -*-
import scrapy
import json
from Renrenche.items import CarInfoItem
import sys
reload(sys)
sys.setdefaultencoding("utf-8")
#
# class GuaziImagePipeline(ImagesPipeline):
#     """下载图片"""
#     def get_media_requests(self, item, info):
#         for i in item["car_image"]:
#             scrapy.Request(i)


class CarItemPipeline(object):
    def __init__(self):
        self.f = open("car_info.json","w")

    def process_item(self, item, spider):
        content = json.dumps(dict(item), ensure_ascii=False)+',\n'
        self.f.write(content)

    def close_spider(self, spider):
        self.f.close()