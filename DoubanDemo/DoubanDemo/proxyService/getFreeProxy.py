import requests
from lxml import etree
import re
import os
import random
import agent


class GetFreeProxy:
    """
    引用：https://github.com/jhao104/proxy_pool/blob/master/ProxyGetter/getFreeProxy.py
    使用_，private方法将不会被执行
    """
    headers = {
        'Connection': 'keep-alive',
        'Cache-Control': 'max-age=0',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': random.choice(agent.agents),
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Encoding': 'gzip, deflate, sdch',
        'Accept-Language': 'zh-CN,zh;q=0.8',
    }

    def _getContent(self, url):
        """
        获取etree，通过xpath定位元素
        """
        content = requests.get(
            url=url, headers=self.headers, timeout=30).content
        # print(content)
        return etree.HTML(content)

    def _parse_kuaidaili(self):
        url_list = ('http://www.kuaidaili.com/proxylist/{page}/'.format(
            page=page) for page in range(1, page + 1))
        for url in url_list:
            content = self._getContent(url)
            proxy_list = content.xpath(
                './/div[@id="index_free_list"]//tbody/tr')
            for proxy in proxy_list:
                yield ':'.join(proxy.xpath('./td/text()')[0:2])

    def parse_daili66(self, proxy_number=100):
        url = r"http://m.66ip.cn/mo.php?sxb=&tqsl={}&port=&export=&ktip=&sxa=&submit=%CC%E1++%C8%A1&textarea=".format(
            proxy_number)
        html = requests.get(url, headers=self.headers).content
        # print(html)
        for proxy in re.findall(b'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}:\d{1,5}', html):
            yield proxy.decode('utf-8')

    def parse_youdaili(self, days=1):
        url = 'http://www.youdaili.net/Daili/http/'
        content = self._getContent(url)
        page_url_list = content.xpath(
            './/div[@class="chunlist"]/ul/li/p/a/@href')[0:days]
        for page_url in page_url_list:
            html = requests.get(page_url, headers=self.headers).content
            # print html
            proxy_list = re.findall(
                b'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}:\d{1,5}', html)
            for proxy in proxy_list:
                yield proxy.decode('utf-8')

    def parse_xicidaili(self):
        url_list = ['http://www.xicidaili.com/nn',  # 高匿
                    'http://www.xicidaili.com/nt',  # 透明
                    ]
        for each_url in url_list:
            content = self._getContent(each_url)
            proxy_list = content.xpath('.//table[@id="ip_list"]//tr')
            for proxy in proxy_list:
                yield ':'.join(proxy.xpath('./td/text()')[0:2])

    def _parse_guobanjia(self):
        url = 'http://www.goubanjia.com/free/gngn/index{page}.shtml'
        for page in range(1, 2):
            content = self._getContent(url.format(page=page))
            print(url.format(page=page))
            print(self.headers['User-Agent'])
            # content = open(
            ip_list = content.xpath('//td[@class="ip"]')
            for ip in ip_list:
                print()
                # yield
                # ip.xpath('.//span/text()|.//*[@style="display:inline-block;"]/text()')
                yield ip.xpath('.//text()')

    def parse_haoip(self):
        url = 'http://haoip.cc/tiqu.htm'
        html = requests.get(url, headers=self.headers).content
        for proxy in re.findall(b'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}:\d{1,5}', html):
            yield proxy.decode('utf-8')

if __name__ == '__main__':
    getFree = GetFreeProxy()
    for ip in getFree.parse_xicidaili():
        print(ip)
