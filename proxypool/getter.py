# -*- conding: utf-8 -*-

from proxypool.crawler import Crawler
from proxypool.storer import RedisCli as RedisClient


class Getter(object):
    def __init__(self):
        self.redis = RedisClient()
        self.crawler = Crawler()

    def start(self):
        print('开始运行获取模块...')
        if not self.redis.is_full_limit():
            for item in range(self.crawler.__CrawlFuncCount__):
                callback = self.crawler.__CrawlFunc__[item]
                proxies = self.crawler.get_proxies(callback)
                for proxy in proxies:
                    proxy_str = ":".join([proxy['ip'], proxy['port']])
                    # print(proxy_str)
                    self.redis.add_proxy(proxy_str)


def getter_test():
    cls = Getter()
    cls.start()


if __name__ == '__main__':
    getter_test()

