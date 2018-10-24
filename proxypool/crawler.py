# -*- coding: utf-8 -*-

import requests
from proxypool import settings
from lxml import etree
import re
# import bs4
import pyquery
import urllib.request
from collections import Iterator


class CrawlMetaclass(type):
    def __new__(cls, name, bases, attrs):
        count = 0
        attrs['__CrawlFunc__'] = []
        for k, v in attrs.items():
            if 'crawl' in k:
                attrs['__CrawlFunc__'].append(k)
                count += 1
        attrs['__CrawlFuncCount__'] = count
        # print(attrs.items())
        return type.__new__(cls, name, bases, attrs)


class Crawler(object, metaclass=CrawlMetaclass):

    def get_proxies(self, callback_func):
        # proxies = []
        # for proxy in eval('self.{}()'.format(callback_func)):
        #     proxies.append(proxy)
        # return proxies
        yield from eval('self.{}()'.format(callback_func))

    def crawl_xicidaili(self, pages=1):
        proxy_info = {
            "ip": "",
            "port": "",
            "protocol": "",
            'area': "",
        }
        base_url = "http://www.xicidaili.com/nn/{}"
        # for url in (base_url.format(page) for page in range(1, pages + 1)):
        #     print(url)
        for url in (base_url.format(page) for page in range(1, pages + 1)):
            response = requests.get(url=url, headers=settings.HEADERS, timeout=2)
            if response.status_code == 200:
                html = etree.HTML(response.text)
                result = html.xpath('//tr')
                # pagination = html.xpath('//div[@class="pagination"]')
                # current_page = pagination[0].xpath('./em[@class="current"]/text()')[0]
                try:
                    for i in range(1, len(result)):
                        td = result[i].xpath('./td/text()')
                        # print(td)
                        if td[4] == '高匿' and '分钟' not in td[10]:
                            proxy_info['ip'] = td[0]
                            proxy_info['port'] = td[1]
                            proxy_info['protocol'] = td[5].lower()
                            proxy_info['area'] = result[i].xpath('./td/a/text()')[0]
                            yield proxy_info
                            # print(self.proxy_info['area'])
                            # 以下代码是用正则表达式匹配信息筛选, 通用性好, 但是相对会比上面静态的方法耗时
                            # for item in td:
                            #     # print(item)
                            #     ip = re.match("(\d+\.\d+\.\d+\.\d+)$", item)
                            #     port = re.match('(\d+)$', item)
                            #     protocol = re.match('(HTTP.*)', item)
                            #     try:
                            #         print(protocol.group(1), self.proxy_info['protocol'])
                            #     except Exception as e:
                            #         pass
                            # print(proxy_info)
                            # print(td)
                except Exception as e:
                    pass

    def crawl_66daili(self, pages=1):
        proxy_info = {
            "ip": "",
            "port": "",
            "protocol": "",
            'area': "",
        }
        base_url = "http://www.66ip.cn/{}.html"
        for url in (base_url.format(page) for page in range(1, pages + 1)):
            try:
                response = requests.get(url=url, headers=settings.HEADERS, timeout=2)
                if response.status_code == 200:
                    html = pyquery.PyQuery(response.text)
                    trs = html('.containerbox table tr:gt(0)').items()
                    for tr in trs:
                        proxy_info['ip'] = tr.find('td:nth-child(1)').text()
                        proxy_info['port'] = tr.find('td:nth-child(2)').text()
                        proxy_info['protocol'] = 'http'
                        yield proxy_info
                        # print(proxy_info)
            except Exception as e:
                print("Error: ", e)
            # print(response.text)


if __name__ == '__main__':
    cra = Crawler()
    # for item in cra.crawl_xicidaili(1):
    #     print(':'.join([item['ip'], item['port']]))

