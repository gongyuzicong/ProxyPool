# -*- conding: utf-8 -*-

from proxypool.crawler import Crawler
from proxypool.storer import RedisCli as RedisClient



class Getter(object):
    def __init__(self):
        self.redis = RedisClient()
        self.crawler = Crawler()

    def run(self):
        print('Getter beging running...')
        if not self.redis.is_full_limit():
            for item in range(self.crawler.__CrawlFuncCount__):
                callback = self.crawler.__CrawlFunc__[item]
                proxies = self.crawler.get_proxies(callback)
                for proxy in proxies:
                    print(proxy)






if __name__ == '__main__':
    cls = Getter()
    cls.run()

