# -*- coding: utf-8 -*-
import json
from datetime import datetime
from elasticsearch import Elasticsearch
from elasticsearch_dsl import Search

client = Elasticsearch(
    ['10.211.55.121:9200']
)
print client.indices.create(index='smurfs', ignore=400)
#
# s = Search(using=client)
#
# s.query("match", title="python")
# response = s.execute()
#
# print response
