import scrapy
from scrapy import Request
from DoubanDemo.items import MovieItem
import random
import re


class MovieSpider(scrapy.Spider):
    name = 'douban_movie'
    HEADERS = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Cache-Control': 'no-cache',
        'Accept-Encoding': 'gzip, deflate, sdch, br',
        'Accept-Language': 'zh-CN,zh;q=0.8',
        'Connection': 'keep-alive',
        'Host': 'movie.douban.com',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': '',
    }

    def start_requests(self):
        tags = ['爱情', '喜剧', '剧情']
        url = r'https://movie.douban.com/tag/'
        # yield Request(url, headers=self.HEADERS)
        for tag in tags:
            yield Request(url + tag, headers=self.HEADERS)

    def parse(self, response):
        print(response.url)
        pass
        movies = response.xpath('//tr[@class="item"]')
        for movie in movies:
            movie_url = movie.xpath('.//a[@class="nbg"]/@href').extract_first()
            # print(movie_url)
            yield Request(movie_url, meta={'dont_redirect': True, 'handle_httpstatus_list': [302]}, headers=self.HEADERS, callback=self.parse_movie)

        for next_url in response.xpath('//span[@class="next"]/a/@href').extract():
            yield Request(next_url, meta={'dont_redirect': True, 'handle_httpstatus_list': [302]}, headers=self.HEADERS)

    def parse_movie(self, response):
        item = MovieItem()
        item['movie_name'] = response.xpath(
            '//h1/span[@property="v:itemreviewed"]/text()').extract_first().split(' ')
        info_xpath = response.xpath('//div[@id="info"]')
        item['director'] = info_xpath.xpath(
            '//a[@rel="v:directedBy"]/text()').extract_first()
        item['screenwriter'] = info_xpath.xpath(
            './/span[2]/span[2]/a/text()').extract()
        # item['screenwriter'] = response.xpath(
        #     '//div[@id="info"]/span[2]/span[2]/a/text()').extract()
        item['starring'] = info_xpath.xpath(
            '//a[@rel="v:starring"]/text()').extract()
        item['movie_type'] = info_xpath.xpath(
            '//span[@property="v:genre"]/text()').extract()
        item['time_release'] = info_xpath.xpath(
            '//span[@property="v:initialReleaseDate"]/text()').extract()
        item['movie_time'] = info_xpath.xpath(
            '//span[@property="v:runtime"]/text()').extract_first()
        item['imdd'] = info_xpath.xpath(
            './a[last()]/@href').extract_first()

        item['rating_num'] = response.xpath(
            '//strong[@property="v:average"]/text()').extract_first()
        item['rating_people'] = response.xpath(
            '//a[@class="rating_people"]/span/text()').extract_first()
        item['movie_url'] = response.url
        # 获取到全部文字
        info_text = info_xpath.xpath('string(.)').extract_first()
        item['area'] = re.compile(
            r'(.|\n)*制片国家/地区: (.*)').match(info_text).group(2).replace(' ', '').split('/')
        item['language'] = re.compile(
            r'(.|\n)*语言: (.*)').match(info_text).group(2).replace(' ', '').split('/')
        yield item

    def errback_http(self, failure):
        request = failure.request
        print('errbacl_http:', request.meta)
