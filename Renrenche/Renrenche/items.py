# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class CarInfoItem(scrapy.Item):
    """车辆的简要信息"""
    # 汽车的名字
    car_name = scrapy.Field()
    # 汽车的价格
    car_price = scrapy.Field()
    # 汽车的原价
    original_price = scrapy.Field()
    # 汽车的链接
    car_link = scrapy.Field()
    # 上牌日期
    car_year = scrapy.Field()
    # 汽车里程
    car_mileage = scrapy.Field()



class CarDetailItem(scrapy.Item):
    """车辆详细情况的类"""
    # 车辆基本参数
    basic_parameter = scrapy.Field()
    # 发动机参数
    engine_parameter = scrapy.Field()
    # 变速箱参数
    transmission = scrapy.Field()
    # 底盘及制动
    chassis = scrapy.Field()
    # 制动参数
    brake = scrapy.Field()
    # 安全配置
    security_configuration = scrapy.Field()
    # 操控配置
    handling = scrapy.Field()
    # 外部配置
    external_configuration = scrapy.Field()
    # 内部配置
    internal_configuration = scrapy.Field()
    # 座椅配置
    seat_configuration = scrapy.Field()
    # 多媒体
    media_configuration = scrapy.Field()
    # 灯光配置
    light_configuration = scrapy.Field()
    # 车窗配置
    window_configuration = scrapy.Field()
    # 制冷设备
    refrigeration = scrapy.Field()
    # 高科技配置
    technology = scrapy.Field()