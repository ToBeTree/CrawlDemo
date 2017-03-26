import requests
from lxml import etree
from bs4 import BeautifulSoup
import re

from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)


class CrawlMovie:
    def __init__(self):
        pass


def getContent():
    headers = {}
    headers[
        'User-Agent'] = 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36'
    url = 'https://movie.douban.com/subject/25934014/'
    r = requests.get(url, headers=headers)
    return r.content


def analysis():
    html = getContent()
    body = etree.HTML(html)
    text_body = body.xpath('//div[@id="info"]/text()')
    aa = body.xpath('//div[@id="info"]')
    print(text_body)
    print(body.xpath('//div[@id="info"]/span[@property="v:genre"]/text()'))
    info = aa[0].xpath('string(.)')
    # print(info)
    info1 = """
        导演: 达米恩·查泽雷
        编剧: 达米恩·查泽雷
        主演: 瑞恩·高斯林 / 艾玛·斯通 / 约翰·传奇 / 罗丝玛丽·德薇特 / 芬·维特洛克 / 杰西卡·罗德 / 水野索诺娅 / 考莉·赫尔南德斯 / J·K·西蒙斯 / 汤姆·艾弗瑞特·斯科特 / 米根·费伊 / 达蒙·冈普顿 / 贾森·福克斯 / 乔什·平茨 / 艾米·科恩 / 特里·沃尔特斯 / 汤姆·谢尔顿 / 辛达·亚当斯 / 克劳丁·克劳迪奥 / D·A·瓦拉赫 / 特雷弗·里斯奥尔 / 奥莉维亚·汉密尔顿 / 安娜·查泽雷 / 马里乌斯·代·弗里斯 / 妮科尔·库隆 / 迈尔斯·安德森 / 约翰·辛德曼 / 瓦拉里·雷·米勒 / 基夫·范登·霍伊维尔 / 佐伊·霍尔 / 登普西·帕皮恩 / 辛德拉·车
        类型: 剧情 / 爱情 / 歌舞

        制片国家/地区: 美国
        语言: 英语
        上映日期: 2017-02-14(中国大陆) / 2016-08-31(威尼斯电影节) / 2016-12-25(美国)
        片长: 128分钟
        又名: 星声梦里人(港) / 乐来越爱你(台) / 爵士情缘 / 啦啦之地
        IMDb链接: tt3783958

    """
    # a =re.compile(r'\d')
    # print(info)
    # info = '语言: hanzi'
    print(type(info))
    area = re.compile(r'(.|\n)*制片国家/地区: (.*)').match(info).group(2)
    print(type(area), area)
    language = re.compile(r'(.|\n)*语言: (.*)').match(info).group(2)
    print(type(language), language)
    time = re.compile(r'(.|\n)*上映日期: (.*)').match(info).group(2).split('/')[0]
    print(time)


if __name__ == '__main__':
    analysis()
