# -*- coding: utf-8 -*-

from snownlp import SnowNLP


class EmotionsUtil(object):
    def extract_sentiments(self, text):
        s = SnowNLP(text.decode("utf-8"))
        sentiment = float(s.sentiments)
        if sentiment > 0.6:
            sentiment = "正"
        elif sentiment > 0.45:
            sentiment = "中"
        else:
            sentiment = "负"
        return sentiment
