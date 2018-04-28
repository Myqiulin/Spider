# -*- coding: utf-8 -*-
import time

import self
from hbase import Hbase
from hbase.ttypes import *
from scrapy.exceptions import NotConfigured
from thrift.transport import TSocket
from smurfs.util.text_util import TextUtil
from smurfs.item.items import ArticleItem, TweetsItem, PersonItem, CommentItem


class HBasePipeline(object):
    def __init__(self, hbase_thrift_server, hbase_thrift_port):
        self.hbase_thrift_server = hbase_thrift_server
        self.hbase_thrift_port = hbase_thrift_port
        self.partitions = self.generat_partition_seed()

        self.transport = TSocket.TSocket(self.hbase_thrift_server, self.hbase_thrift_port)
        self.transport = TTransport.TBufferedTransport(self.transport)
        protocol = TBinaryProtocol.TBinaryProtocol(self.transport)

        self.client = Hbase.Client(protocol)

    @classmethod
    def from_crawler(cls, crawler):
        if not crawler.settings.getbool('HBASE_PIPELINE_ENABLED'):
            raise NotConfigured

        return cls(
            hbase_thrift_server=crawler.settings.get("HBASE_THRIFT_SERVER"),
            hbase_thrift_port=crawler.settings.get("HBASE_THRIFT_PORT"),
        )

    def open_spider(self, spider):
        print 'into HBasePipeline.'

    def close_spider(self, spider):
        if self.transport and self.transport.isOpen():
            self.transport.close()
        print 'close HBasePipeline...'

    def generat_partition_seed(self):
        arr = list([])
        for i in range(0, 10):
            arr.append(str(i))
        for i in range(ord("A"), ord("Z") + 1):
            arr.append(chr(i))
        for i in range(ord("a"), ord("z") + 1):
            arr.append(chr(i))
        partitions = list([])
        for i in range(0, len(arr)):
            for j in range(0, len(arr)):
                partitions.append('%s%s' % (arr[i], arr[j]))

        return partitions

    def generator_rowkey(self, key, return_byte=False):
        if not key:
            return None
        i = abs(hash(key) % len(self.partitions))
        rowkey = '%s-%s' % (self.partitions[i], key)
        if not return_byte:
            return rowkey
        else:
            return bytes(rowkey)

    def process_item(self, item, spider):
        # if isinstance(item, ArticleItem) is False and isinstance(item, TweetsItem) is False:
        #     return item
        if isinstance(item, ArticleItem):
            self.insert_article(item)
        if isinstance(item, PersonItem):
            self.insert_person(item)
        if isinstance(item, CommentItem):
            self.insert_comment(item)
        if isinstance(item, TweetsItem):
            self.insert_tweets(item)
            pass
        return item

    def insert_person(self, item):
        if item.get("nikename") and len(item.get("nikename")) > 0:
            try:
                self.transport.open()
                nikename = item.get("nikename")
                follow_count = item.get("follow_count")
                fans_count = item.get("fans_count")
                tweets_count = item.get("tweets_count")
                tags = item.get("tags")
                gender = item.get("gender")
                # str = long(round(time.time() * 1000))
                rowkey = self.generator_rowkey(long(round(time.time() * 1000)))
                muttitle = Mutation(column=bytes('f1:nikename'), value=bytes(nikename))
                mutsrc = Mutation(column=bytes('f1:follow_count'), value=bytes(follow_count))
                muttype = Mutation(column=bytes('f1:fans_count'), value=bytes(fans_count))
                mutcontent = Mutation(column=bytes('f1:tweets_count'), value=bytes(tweets_count))
                mutdate = Mutation(column=bytes('f1:tags'), value=bytes(tags))
                mutwbid = Mutation(column=bytes('f1:gender'), value=bytes(gender))
                self.client.mutateRow('TB_PERSON', rowkey, [muttitle, mutsrc, muttype, mutcontent,
                                                            mutdate, mutwbid])
            except Exception, e:
                pass
            finally:
                if self.transport and self.transport.isOpen():
                    self.transport.close()

    def insert_tweets(self, item):
        if item.get("id") and len(item.get("id")) > 0:
            try:
                self.transport.open()
                textutil = TextUtil()

                infoId = item.get("id")  # 每条微博的ID
                text = textutil.format_text(item.get("text"))
                infoContent = text.decode("utf-8")
                infoSrc = ("http://m.weibo.cn/u/%s" % item["uid"])
                infoTitle = item.get("title")
                infoSource = item.get("source")
                infoDate = item.get("create_time")
                infoType = "微博".decode("utf-8")
                infoTag = item.get("tags")
                # str = long(round(time.time() * 1000))
                rowkey = self.generator_rowkey(str(infoId)[::-1])
                muttitle = Mutation(column=bytes('f1:infoTitle'), value=bytes(infoTitle))
                mutsrc = Mutation(column=bytes('f1:infoSrc'), value=bytes(infoSrc))
                muttype = Mutation(column=bytes('f1:infoType'), value=bytes(infoType))
                mutcontent = Mutation(column=bytes('f1:infoContent'), value=bytes(infoContent))
                mutsource = Mutation(column=bytes('f1:infoSource'), value=bytes(infoSource))
                mutdate = Mutation(column=bytes('f1:infoDate'), value=bytes(infoDate))
                mutid = Mutation(column=bytes('f1:infoId'), value=bytes(infoId))
                muttag = Mutation(column=bytes('f1:infoTag'), value=bytes(infoTag))
                self.client.mutateRow('TB_INFORMATIONS', rowkey, [muttitle, mutsrc, muttype, mutcontent, mutsource,
                                                                  mutdate, mutid, muttag])
            except Exception, e:
                pass
            finally:
                if self.transport and self.transport.isOpen():
                    self.transport.close()

    def insert_article(self, item):
        if item.get("text") and len(item.get("text")) > 0:
            try:
                self.transport.open()
                infoTitle = item.get("title")
                infoSrc = item.get("url")
                infoType = item.get("type")
                infoContent = item.get("content")
                infoText = item.get("text")
                infoDesc = item.get("desc")
                infoDate = item.get("pub_date")
                infoTag = item.get("tags")
                # infoEntity = item.get("entity")
                infoAuthor = item.get("author")
                infoId = item.get("id")

                str = long(round(time.time() * 1000))
                rowkey = self.generator_rowkey(str(infoId)[::-1])
                print rowkey
                muttitle = Mutation(column=bytes('f1:infoTitle'), value=bytes(infoTitle))
                mutsrc = Mutation(column=bytes('f1:infoSrc'), value=bytes(infoSrc))
                muttype = Mutation(column=bytes('f1:infoType'), value=bytes(infoType))
                mutcontent = Mutation(column=bytes('f1:infoContent'), value=bytes(infoContent))
                muttext = Mutation(column=bytes('f1:infoText'), value=bytes(infoText))
                mutdesc = Mutation(column=bytes('f1:infoDesc'), value=bytes(infoDesc))
                mutdate = Mutation(column=bytes('f1:infoDate'), value=bytes(infoDate))
                muttag = Mutation(column=bytes('f1:infoTag'), value=bytes(infoTag))
                # mutentity = Mutation(column=bytes('f1:infoEntity'), value=bytes(infoEntity))
                mutauthor = Mutation(column=bytes('f1:infoAuthor'), value=bytes(infoAuthor))
                mutid = Mutation(column=bytes('f1:infoId'), value=bytes(infoId))
                self.client.mutateRow('TB_INFORMATIONS', rowkey, [muttitle, mutsrc, muttype, mutcontent, muttext,
                                                                  mutdesc, mutdate, muttag, mutauthor,
                                                                  mutid])

            except Exception, e:
                pass
            finally:
                if self.transport and self.transport.isOpen():
                    self.transport.close()

    def insert_comment(self, item):

        if item.get("com_text") and len(item.get("com_text")) > 0:
            try:
                self.transport.open()
                infoId = item.get("info_id")
                commentId = item.get("com_id")
                commentText = item.get("com_text")
                commentContent = item.get("com_content")
                commentDate = item.get("com_time")
                commentUserInfo = item.get("com_userinfo")
                commentUserName = item.get("com_username")
                commentEmotions = item.get("com_sentiments")
                commentKeyWord = item.get("tags")
                commentLiked = item.get("com_liked")
                commentLocation = item.get("com_location")
                if commentLocation is None and commentLocation == "":
                    commentLocation = "其他"

                # str = long(round(time.time() * 1000))
                rowkey = self.generator_rowkey(str(commentId)[::-1])

                print rowkey
                mutId = Mutation(column=bytes('f1:infoId'), value=bytes(infoId))
                mutText = Mutation(column=bytes('f1:commentText'), value=bytes(commentText))
                mutContent = Mutation(column=bytes('f1:commentContent'), value=bytes(commentContent))
                mutDate = Mutation(column=bytes('f1:commentDate'), value=bytes(commentDate))
                mutUserInfo = Mutation(column=bytes('f1:commentUserInfo'), value=bytes(commentUserInfo))
                mutUserName = Mutation(column=bytes('f1:commentUserName'), value=bytes(commentUserName))
                mutEmotions = Mutation(column=bytes('f1:commentEmotions'), value=bytes(commentEmotions))
                mutKeyWord = Mutation(column=bytes('f1:commentKeyWord'), value=bytes(commentKeyWord))
                mutLiked = Mutation(column=bytes('f1:commentLiked'), value=bytes(commentLiked))
                mutLocation = Mutation(column=bytes('f1:commentLocation'), value=bytes(commentLocation))
                self.client.mutateRow('TB_INFORMATIONCOMMENTS', rowkey, [mutId, mutText, mutContent, mutDate, mutUserInfo,
                                                                  mutUserName, mutEmotions, mutKeyWord, mutLiked,
                                                                  mutLocation])

            except Exception, e:
                pass
            finally:
                if self.transport and self.transport.isOpen():
                    self.transport.close()