# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from Renrenche.items import CarInfoItem

class RenrenSpider(CrawlSpider):
    name = 'renrenche'
    allowed_domains = ['renrenche.com']
    start_urls = ['https://www.renrenche.com/sh/ershouche/']
    rules = (
        Rule(LinkExtractor(allow=r'/sh/ershouche/p'),callback='parse_item',follow=True),
        Rule(LinkExtractor(allow=r'/sh/car/'), callback='parse_detail', follow=False),
    )

    def parse_item(self, response):
        car_list = response.xpath("//ul[@class='row-fluid list-row js-car-list']/li/a")
        for car in car_list:
            item = CarInfoItem()
            # 汽车的名字
            item['car_name'] = car.xpath("./h3/text()").extract()
            # 汽车的价格
            # car_price = scrapy.Field()
            # 汽车的原价
            yuanjia = car.xpath(".//div[@class='new-price']/span/text()").extract()[0]
            if yuanjia:
                item['original_price'] = yuanjia
            else:
                item['original_price'] = "null"
            # 汽车的链接
            item['car_link'] = "http://www.renrenche.com"+car.xpath("./@href").extract()[0]
            # 上牌日期
            item['car_year'] = car.xpath(".//span[@class='basic']/text()").extract()[0]
            # 汽车里程
            item['car_mileage'] = car.xpath(".//span[@class='basic']/text()").extract()[1]

            yield item
    def parse_detail(self, response):

        basic_list = response.xpath("//table[@id='basic-parms']/tbody").extract()
        for basic in basic_list:

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
