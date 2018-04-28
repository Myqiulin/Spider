# -*- coding: utf-8 -*-
import os
import sys

from nltk.tag import StanfordNERTagger
from nltk.tokenize import StanfordSegmenter
from smurfs.util.common import is_linux

# System env setting
project_path = os.path.split(os.path.realpath(sys.path[0]))[0]
if project_path.find("smurfs") == -1:
    project_path += "/smurfs"
stanford_nlp_path = "%s/stanford_nlp" % project_path
stanford_nlp_jars_path = ".;%s/stanford-segmenter.jar;%s/stanford-ner.jar;%s/slf4j-api.jar" % (stanford_nlp_path, stanford_nlp_path, stanford_nlp_path)
sys_flag = ";"
if is_linux():
    sys_flag = ":"
    stanford_nlp_jars_path = ".:%s/stanford-segmenter.jar:%s/stanford-ner.jar:%s/slf4j-api.jar" % (stanford_nlp_path, stanford_nlp_path, stanford_nlp_path)


class NLPToolkit(object):
    segmenter = None
    ner_tagger = None

    def __init__(self):
        os.environ["STANFORD_MODELS"] = stanford_nlp_path
        os.environ["STANFORD_CORENLP"] = stanford_nlp_path
        classpath = os.environ.get("CLASSPATH")
        if classpath is None:
            classpath = ""
        os.environ["CLASSPATH"] = "%s%s%s" % (stanford_nlp_jars_path, sys_flag, classpath)

        self.segmenter = StanfordSegmenter(
            path_to_sihan_corpora_dict="%s/data/" % stanford_nlp_path,
            path_to_model="%s/data/pku.gz" % stanford_nlp_path,
            path_to_dict="%s/data/dict-chris6.ser.gz" % stanford_nlp_path,
        )

        self.ner_tagger = StanfordNERTagger('chinese.misc.distsim.crf.ser.gz')

    def getStanfordSegmenter(self):
        return self.segmenter

    def getStanfordNERTagger(self):
        return self.ner_tagger
