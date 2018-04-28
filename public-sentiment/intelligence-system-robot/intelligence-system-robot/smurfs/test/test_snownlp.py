# -*- coding: utf-8 -*-
from snownlp import SnowNLP

from smurfs.util.text_util import TextUtil

text = """我喜欢刘亦菲，不做作了，还很美"""
s = SnowNLP(text.decode("utf-8"))
# print s.keywords(3)
print s.sentiments

util = TextUtil()
print util.extract_sentiments(text)


