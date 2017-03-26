# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/spider-middleware.html

from scrapy import signals

import sys
import random
import time
import logging
# 需要使用sys，将要导入模块路径添加进来
# sys.path.append('..')
from proxyService.agent import agents
from proxyService.proxyService import Proxy

# from scrapy.exceptions import

log = logging.getLogger('scrapy.proxies')


class DoubandemoSpiderMiddleware(object):
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the spider middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_spider_input(response, spider):
        # Called for each response that goes through the spider
        # middleware and into the spider.

        # Should return None or raise an exception.
        return None

    def process_spider_output(response, result, spider):
        # Called with the results returned from the Spider, after
        # it has processed the response.

        # Must return an iterable of Request, dict or Item objects.
        for i in result:
            yield i

    def process_spider_exception(response, exception, spider):
        # Called when a spider or process_spider_input() method
        # (from other spider middleware) raises an exception.

        # Should return either None or an iterable of Response, dict
        # or Item objects.
        pass

    def process_start_requests(start_requests, spider):
        # Called with the start requests of the spider, and works
        # similarly to the process_spider_output() method, except
        # that it doesn’t have a response associated.

        # Must return only requests (not items).
        for r in start_requests:
            yield r

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)


# 自定义下载中间件
class ProxyMiddleware(object):
    def __init__(self, settings):
        self.retry_http_codes = set(int(x)
                                    for x in settings.getlist('RETRY_HTTP_CODES'))
        self.proxyPool = Proxy()
        self.chose_proxy = ''
    # 导入设置，暂时不需要使用

    @classmethod
    def from_crawler(cls, crawler):
        return cls(crawler.settings)

    # 每个request通过下载中间件时，该方法被调用
    def process_request(self, request, spider):
        # proxy = self.proxyPool.get_proxy()
        # try:
        #     if proxy:
        #         # print(type(proxy), "ip is", proxy)
        #         request.meta['proxy'] = "http://%s" % proxy
        #         print('request.meta:', request.meta)
        #         # if request.meta['retry_times'] > 3:
        #         #     # 重试次数超过3次，删除该代理
        #         #     self.proxyPool.delete_proxy(proxy)
        #     else:
        #         print('start refresh proxy pool, please wait...')
        #         self.proxyPool.refresh_proxy()
        #         time.sleep(150)  # 等待代理池更新
        #         proxy = self.proxyPool.get_proxy()
        #         request.meta['proxy'] = "http://%s" % proxy
        # except Exception as e:
        #     print('proxyException: %s' % proxy)
        #     self.proxyPool.delete_proxy(proxy)
        #     proxy = self.proxyPool.get_proxy()
        #     request.meta['proxy'] = "http://%s" % proxy
        if 'proxy' in request.meta:  # 　判断request是否设置了代理
            log.debug('proxy already in request.meta')
            if request.meta['exception'] is False:
                log.debug('request.meta["exception"] is %s, not change proxy agin' %
                          request.meta['exception'])
                return
        request.meta['exception'] = False
        if self.chose_proxy == '':
            self.chose_proxy = self.proxyPool.get_proxy()
        if self.chose_proxy is None:
            self.chose_proxy = self.wait_proxy_refresh()
        log.debug('using proxy <%s>' % self.chose_proxy)
        request.meta['proxy'] = "http://%s" % self.chose_proxy

    def process_response(self, request, response, spider):
        if response.status in [302, 301]:  # 尝试在Response处理重定向
            log.debug('url <%s> before redirect' % request)
            #TODO
        if response.status in self.retry_http_codes:
            retries = request.meta.get('retry_times', 0)
            if retries >= 5:
                log.debug('proxy <%s> is retry <%s> times' %
                          (self.chose_proxy, retries))
                self.change_proxy()
                request.meta['proxy'] = "http://%s" % self.chose_proxy
                log.debug('change proxy <%s> in process_response' %
                          self.chose_proxy)
                request.meta['retry_times'] = 0  # 　重设重试次数
                return request  # 返回request相当于重新调度一次
        return response

    def process_exception(self, request, exception, spider):
        if 'proxy' not in request.meta:
            return
        request.meta['exception'] = True
        proxy = request.meta['proxy']
        log.debug('remove invail proxy <%s>' % proxy)
        self.proxyPool.delete_proxy(proxy.split('/')[-1])
        self.chose_proxy = self.proxyPool.get_proxy()
        if self.chose_proxy is None:
            self.chose_proxy = self.wait_proxy_refresh()
        log.debug('now using <%s>' % self.chose_proxy)

    def change_proxy(self):
        log.debug('change proxy')
        self.chose_proxy = self.proxyPool.get_proxy()
        if self.chose_proxy is None:
            self.chose_proxy = self.wait_proxy_refresh()

    def wait_proxy_refresh(self):
        log.debug('proxy is null, wait for crawl agin...')
        self.proxyPool.refresh_proxy()
        time.sleep(120)  # 等待系统更新代理池
        proxy = self.proxyPool.get_proxy()
        if proxy is None:
            raise 'Proxy pool error'
        return proxy


class AgentMiddleware(object):

    def process_request(self, request, spider):
        request.headers['User-Agent'] = random.choice(agents)
        # print(request.headers)
