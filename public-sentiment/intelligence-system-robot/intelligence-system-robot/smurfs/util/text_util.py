# -*- coding: utf-8 -*-
import jieba
import jieba.analyse
import jieba.posseg
from bs4 import BeautifulSoup
from bs4 import Comment
from snownlp import SnowNLP

from nlp_toolkit import NLPToolkit
from nlp_toolkit import project_path
from smurfs.util.common import is_linux


class TextUtil(object):
    nlp = NLPToolkit()

    def __int__(self):
        stop_words_file = ('%s/stanford_nlp/dict/stop_words.txt' % project_path)
        dict_words_file = ('%s/stanford_nlp/dict/dict.txt.big.txt' % project_path)
        jieba.set_dictionary(dict_words_file)
        jieba.analyse.set_stop_words(stop_words_file)
        jieba.initialize()
        if is_linux():
            jieba.enable_parallel(10)

    def extract_tags(self, text):
        tags_list = jieba.analyse.extract_tags(text, topK=20, allowPOS=('ns', 'n', 'vn', 'v', 'nr', 'nt'))
        tags = ",".join(tags_list)
        return tags

    def extract_entity(self, text):
        entity = list([])
        words = self.nlp.getStanfordSegmenter().segment(text.decode("utf-8"))
        tags_list = jieba.analyse.extract_tags(text, topK=20, allowPOS=('ns', 'n', 'vn', 'v', 'nr', 'nt'))
        tags_str = " ".join(tags_list)

        res = self.nlp.getStanfordNERTagger().tag(words.split())
        res2 = self.nlp.getStanfordNERTagger().tag(tags_str.split())
        res.extend(res2)
        for word, tag in res:
            tag = tag.lower()
            if tag == "location" or tag == "person" or (tag == "organization" and len(word) > 1) or (
                            tag == "misc" and len(word) > 1):
                entity.append(("%s:%s" % (word, tag)))
        return entity

    def extract_desc(self, text, len):
        return text[0: len] + "..."

    def format_html(self, content):
        soup = BeautifulSoup(str(content).replace("\r", "").replace("\n", "").strip(), "lxml")
        tags = soup.find_all(True)
        for tag in tags:
            del tag.attrs
            if type(tag.string) is Comment:
                tag.decompose()
            if str(tag.name).lower() == "script":
                tag.decompose()
            if str(tag.name).lower() == "iframe":
                tag.decompose()
        html = str(soup).strip()
        return html

    def format_text(self, html):
        soup = BeautifulSoup(html, "lxml")
        return soup.get_text().strip()

    def extract_sentiments(self, text):
        s = SnowNLP(text)

        sentiment = float(s.sentiments)
        if sentiment > 0.6:
            sentiment = "正"
        elif sentiment > 0.45:
            sentiment = "正"
        else:
            sentiment = "正"
        return sentiment
