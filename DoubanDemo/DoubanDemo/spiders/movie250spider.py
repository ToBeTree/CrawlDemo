import scrapy
from DoubanDemo.items import Movie250Item
from scrapy import Request


class Movie250Spider(scrapy.Spider):
    name = 'movie_250'
    url = 'https://movie.douban.com/subject/1292052/'
    headers = {}
    headers[
        'User-Agent'] = 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36'

    def start_requests(self):
        yield Request(self.url, headers=self.headers)

    # @staticmethod
    def parse(self, response):
        item = Movie250Item()
        # 获取电影地址，re是汉字识别
        area = response.xpath(
            '//div[@id="info"]/text()').re(r'[\u4e00-\u9fa5]+$')[0]
        print('fuck', area)
        yield item
