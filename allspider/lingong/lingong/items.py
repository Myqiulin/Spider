# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class LingongItem(scrapy.Item):
    """路面机械网"""
    title = scrapy.Field()  # 新闻标题
    pub_time = scrapy.Field()  # 发布时间
    content_ori = scrapy.Field()  # 新闻来源
    content = scrapy.Field()  # 新闻内容


class WeiboItem(scrapy.Item):
    """微博"""
    data = scrapy.Field()

class BlogItem(scrapy.Item):
    """博文内容"""
    text = scrapy.Field()  # 博文内容
    p_time = scrapy.Field()  # 发布时间
    trans_total = scrapy.Field()  # 转发数
    com_total = scrapy.Field()  # 评论数
    like_total = scrapy.Field()  # 点赞数
    comment = scrapy.Field()  # 评论


class CommentItem(scrapy.Item):
    """博文评论详情"""
    user_name = scrapy.Field()  # 用户名
    c_time = scrapy.Field()  # 评论时间
    c_like = scrapy.Field()  # 评论点赞数
