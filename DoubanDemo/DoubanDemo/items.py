# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy

# Content-Type:application/x-www-form-urlencoded
# Form Data 传递的数据实际为x-www-form-urlencoded（Postman中）


class DoubandemoItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass


class Movie250Item(scrapy.Item):
    title = scrapy.Field()
    url = scrapy.Field()
    area = scrapy.Field()


class MovieItem(scrapy.Item):
    # 片名
    movie_name = scrapy.Field()
    # 导演
    director = scrapy.Field()
    # 编剧
    screenwriter = scrapy.Field()
    # 主演
    starring = scrapy.Field()
    # 类型
    movie_type = scrapy.Field()
    # 制片地区
    area = scrapy.Field()
    # 语言
    language = scrapy.Field()
    # 上映时间
    time_release = scrapy.Field()
    # 片长
    movie_time = scrapy.Field()
    # imdd链接
    imdd = scrapy.Field()
    # 豆瓣评分
    rating_num = scrapy.Field()
    # 评价总人数
    rating_people = scrapy.Field()
    # 链接地址
    movie_url = scrapy.Field()

    def __repr__(self):
        """only print out attr1 after exiting the Pipeline"""
        return repr({"movie_name": self['movie_name']})
