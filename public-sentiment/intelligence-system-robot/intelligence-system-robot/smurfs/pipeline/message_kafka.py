# -*- coding: utf-8 -*-
# Kafka pipeline
# @author william
# @version 1.0
import json

from kafka import KafkaProducer

from smurfs.item.items import CommentItem


class KafkaPipeline(object):
    """ Kafka pipeline """
    fetch_counter = 0

    def __init__(self, kafka_broker, kafka_topic):
        self.kafka_broker = kafka_broker
        self.kafka_topic = kafka_topic

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            kafka_broker=crawler.settings.get("KAFKA_BROKER_SERVER"),
            kafka_topic=crawler.settings.get("KAFKA_TOPIC_NAME")
        )

    def open_spider(self, spider):
        print 'into KafkaPipeline.'

    def close_spider(self, spider):
        print ('close KafkaPipeline... record num is %d.' % (self.fetch_counter))

    def process_item(self, item, spider):
        if isinstance(item, CommentItem) is False:
            return item
        if isinstance(item, CommentItem):

            producer = KafkaProducer(
                bootstrap_servers=self.kafka_broker,
                value_serializer=lambda v: json.dumps(v).encode("utf-8"),
                compression_type="gzip"
            )
            message = {
                "info_id": item[u'info_id'],
                "com_time": item[u'com_time'],
                "com_id": item[u'com_id'],
                "com_username": item[u"com_username"],
                "com_userinfo": item[u"com_userinfo"],
                "com_userid": item[u"com_userid"],
                "com_liked": item[u"com_liked"],
                "com_text": item[u"com_text"],
                "com_content": item[u"com_content"],
                "com_location": item[u"com_location"],
                "com_source": item[u"com_source"],
                "com_sentiments": item[u"com_sentiments"],
                "com_tags": item[u"com_tags"]
            }
            json_data = json.dumps(message, ensure_ascii=False, encoding='utf-8')
            # future = producer.send(self.kafka_topic, json_data.decode('unicode_escape'))
            print 'self.kafka_topic:%s' % self.kafka_topic
            future = producer.send(self.kafka_topic, message)
            producer.flush()
            if future.is_done:
                self.fetch_counter += 1
            return item
