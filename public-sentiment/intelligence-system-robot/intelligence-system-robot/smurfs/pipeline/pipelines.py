# -*- coding: utf-8 -*-

import json
import codecs

"""
以下pipeline将所有(从所有spider中)爬取到的item，存储到一个独立地 items.jl 文件，
每行包含一个序列化为JSON格式的item:
"""


class TutorialPipeline(object):
    def __init__(self):
        print "sfcdds"
        self.file = codecs.open('data.json', mode='wb', encoding='utf-8')  # 数据存储到data.json

    def process_item(self, item, spider):
        line = json.dumps(dict(item)) + "\n"
        self.file.write(line.decode("unicode_escape"))
        return item
