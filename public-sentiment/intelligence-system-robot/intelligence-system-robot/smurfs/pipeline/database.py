# -*- coding: utf-8 -*-
# mysql pipeline
# @author william
# @version 1.0
import mysql.connector
from scrapy.exceptions import NotConfigured

from smurfs.item.items import PersonItem, TweetsItem, RelationshipsItem, WechatUserItem


class DBPipeline(object):
    """ mysql pipeline """

    def __init__(self, mysql_server_ip, mysql_server_port, mysql_conn_timeout, mysql_server_user, mysql_server_password, mysql_server_db):
        self.mysql_server_ip = mysql_server_ip
        self.mysql_server_port = mysql_server_port
        self.mysql_conn_timeout = mysql_conn_timeout
        self.mysql_server_user = mysql_server_user
        self.mysql_server_password = mysql_server_password
        self.mysql_server_db = mysql_server_db

        self.conn = mysql.connector.connect(host=mysql_server_ip,
                                            port=mysql_server_port,
                                            user=mysql_server_user,
                                            password=mysql_server_password,
                                            database=mysql_server_db,
                                            charset="utf8")

    @classmethod
    def from_crawler(cls, crawler):
        if not crawler.settings.getbool('MYSQL_PIPELINE_ENABLED'):
            raise NotConfigured

        return cls(
            mysql_server_ip=crawler.settings.get("MYSQL_SERVER_IP"),
            mysql_server_port=crawler.settings.get("MYSQL_SERVER_PORT"),
            mysql_conn_timeout=crawler.settings.get("MYSQL_CONN_TIMEOUT"),
            mysql_server_user=crawler.settings.get("MYSQL_SERVER_USER"),
            mysql_server_password=crawler.settings.get("MYSQL_SERVER_PASSWORD"),
            mysql_server_db=crawler.settings.get("MYSQL_SERVER_DB"),
        )

    def open_spider(self, spider):
        print "into DBPipeline."

    def close_spider(self, spider):
        if self.conn:
            self.conn.close()
        print "close DBPipeline."

    def process_item(self, item, spider):
        # print json.dumps(dict(item), ensure_ascii=False)
        if isinstance(item, PersonItem):
            self.insert_person(item)
        if isinstance(item, TweetsItem):
            self.insert_tweets(item)
        if isinstance(item, RelationshipsItem):
            self.insert_relation(item)
        if isinstance(item, WechatUserItem):
            self.insert_wechat(item)
        return item

    def insert_person(self, item):
        cursor = None
        person = dict(item)
        try:
            cursor = self.conn.cursor()
            sql = """
                    INSERT INTO `tb_person` (`uid`, `nikename`, `gender`, `province`, `city`, `tags`, `level`, `description`,
                    `email`, `sunshine_credit`, `registration`, `school`, `verified`, `verified_reason`, `tweets_count`, `follow_count`, `fans_count`)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                """
            param = (person.get("uid", ""), person.get("nikename", ""), person.get("gender", ""), person.get("province", ""), person.get("city", ""), person.get("tags", ""), person.get("level", ""),
                     person.get("description", ""), person.get("email", ""), person.get("sunshine_credit", ""), person.get("registration", ""), person.get("school", ""), person.get("verified", ""), person.get("verified_reason", ""),
                     person.get("tweets_count", ""), person.get("follow_count", ""), person.get("fans_count", ""))
            cursor.execute(sql, param)
            self.conn.commit()
        except Exception, e:
            if cursor:
                cursor.close()

    def insert_tweets(self, item):
        cursor = None
        tweets = dict(item)
        try:
            cursor = self.conn.cursor()
            sql = """
                    INSERT INTO `tb_tweets` (`id`, `uid`, `bid`, `location`, `source`, `text`, `comments_count`,
                    `attitudes_count`, `reposts_count`, `create_time`,`company`,`blog`) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                """
            param = (tweets.get("id", ""), tweets.get("uid", ""), tweets.get("bid", ""), tweets.get("location", ""), tweets.get("source", ""),
                     tweets.get("text", ""), tweets.get("comments_count", ""),
                     tweets.get("attitudes_count", ""), tweets.get("reposts_count", ""), tweets.get("create_time", ""), tweets.get("company", ""), tweets.get("blog", ""))
            cursor.execute(sql, param)
            self.conn.commit()
        except Exception, e:
            if cursor:
                cursor.close()

    def insert_relation(self, item):
        pass

    def insert_wechat(self, item):
        cursor = None
        wechat = dict(item)
        try:
            cursor = self.conn.cursor()
            sql = """
                    INSERT INTO `tb_wechat` (`wid`, `nikename`, `description`, `authentication`, `profile_url`) VALUES (%s,%s,%s,%s,%s)
               """
            param = (wechat.get("wid", ""), wechat.get("nikename", ""), wechat.get("description", ""), wechat.get("authentication", ""), wechat.get("profile_url", ""))
            cursor.execute(sql, param)
            self.conn.commit()
        except Exception, e:
            if cursor:
                cursor.close()
