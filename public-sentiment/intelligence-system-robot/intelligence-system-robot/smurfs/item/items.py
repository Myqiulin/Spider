# -*- coding: utf-8 -*-
# All items define
# @author william
# @version 1.0
from scrapy import Item, Field


# 文章类型的Item
class ArticleItem(Item):
    id = Field()
    title = Field()
    url = Field()
    content = Field()
    author = Field()
    type = Field()
    text = Field()
    desc = Field()
    pub_date = Field()
    tags = Field()
    entity = Field()
    hash = Field()
    source = Field()


# 微信公众号
class WechatUserItem(Item):
    wid = Field()
    nikename = Field()
    description = Field()
    authentication = Field()
    profile_url = Field()


# 微博内容
class TweetsItem(Item):
    id = Field()  # 内容ID
    uid = Field()  # 用户ID
    bid = Field()  # 微博ID
    title = Field()  # 微博标题
    location = Field()  # 位置
    source = Field()  # 来源
    content = Field()  # 内容
    text = Field()  # 内容
    tags = Field()  # 关键词
    comments_count = Field()  # 评论次数
    attitudes_count = Field()  # 赞次数
    reposts_count = Field()  # 转发次数
    create_time = Field()  # 创建时间


# 微博用户
class PersonItem(Item):
    uid = Field()  # 用户ID
    description = Field()  # 用户简介
    follow_count = Field()  # 关注人数
    fans_count = Field()  # 粉丝人数
    nikename = Field()  # 用户昵称
    tweets_count = Field()  # 用户微博总数
    verified = Field()  # 是否认证用户
    verified_reason = Field()  # 认证类型
    school = Field()  # 用户学习
    email = Field()  # 用户邮箱
    level = Field()  # 用户等级
    sunshine_credit = Field()  # 阳光信用
    registration = Field()  # 注册时间
    tags = Field()  # 标签
    gender = Field()  # 性别
    province = Field()  # 所在地省份
    city = Field()  # 所在地城市
    company = Field()  # 公司
    blog = Field()  # 博客


# 微博用户关系
class RelationshipsItem(Item):
    follower = Field()
    be_follower = Field()  # 被关注者的ID


# 评论信息
class CommentItem(Item):
    # 文章ID
    info_id = Field()
    # 评论ID
    com_id = Field()
    com_text = Field()
    com_content = Field()
    com_time = Field()
    com_userinfo = Field()
    com_username = Field()
    com_liked = Field()
    com_userid = Field()
    com_location = Field()
    com_sentiments = Field()
    com_tags = Field()
    # 评论来源
    com_source = Field()
