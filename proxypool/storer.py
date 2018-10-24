# -*- coding:utf-8 -*-

import redis
import random
from proxypool import settings
import proxypool.errors


REDIS_KEY = 'proxies'
POOL_UPPER_LIMIT = 10000


class RedisCli(object):
    def __init__(self,
                 host=settings.REDIS_HOST,
                 port=settings.REDIS_PORT,
                 password=settings.REDIS_PWD):
        """
        初始化, 连接Redis
        :param host: Redis数据库地址
        :param port: Redis数据库端口
        :param password: Redis数据库登录密码
        """
        result = self.redis = redis.StrictRedis(host=host, port=port, password=password, decode_responses=True)
        print(result)

    def add_proxy(self, proxy, score=settings.INITIAL_SCORE):
        """
        添加代理
        :param proxy: 代理地址+端口
        :param score: 分值,配合分值管理方法使用
        :return: 添加结果
        """
        if not self.redis.zscore(REDIS_KEY, proxy):
            return self.redis.zadd(REDIS_KEY, score, proxy)

    def get_proxy_random(self):
        """
        随机获取一个代理
        :return: 返回一个代理或者报错
        """
        result = self.redis.zrangebyscore(REDIS_KEY, settings.MAX_LIMIT_SCORE, settings.MAX_LIMIT_SCORE)
        if len(result):
            return random.choice(result)
        else:
            result = self.redis.zrevrange(REDIS_KEY, 0, 100)
            if len(result):
                return random.choice(result)
            else:
                raise proxypool.errors.ProxyEmptyErrors

    def dec_proxy_score(self, proxy):
        """
        代理分数-1
        :param proxy: 代理
        :return: 修改后的分数
        """
        score = self.redis.zscore(REDIS_KEY, proxy)
        if score and score > settings.MINI_LIMIT_SCORE:
            print("代理: {}, 当前分数: {}, 行为: 分数-1".format(proxy, score))
            return self.redis.zincrby(REDIS_KEY, proxy, -1)
        else:
            print("代理: {}, 当前分数: {}, 行为: 删除此代理".format(proxy, score))
            return self.redis.zrem(REDIS_KEY, proxy)

    def proxy_is_exists(self, proxy):
        """
        判断代理是否存在
        :param proxy: 代理
        :return: 存在返回True, 不存在返回False
        """
        if self.redis.zscore(REDIS_KEY, proxy) != None:
            return True
        else:
            return False

    def set_proxy_max_score(self, proxy):
        """
        将代理设置为最大分数值
        :param proxy: 需要设置的代理
        :return: 设置成功与否
        """
        print('代理 {} 可用, 设置分数为: {}'.format(proxy, settings.MAX_LIMIT_SCORE))
        return self.redis.zadd(REDIS_KEY, settings.MAX_LIMIT_SCORE, proxy)

    def get_pool_count(self):
        """
        获取代理池里面代理的数量
        :return: 数量的值
        """
        return self.redis.zcard(REDIS_KEY)

    def get_all_proxy(self):
        """
        获取代理池里面所有的代理
        :return: 全部代理列表
        """
        return self.redis.zrangebyscore(REDIS_KEY, settings.MINI_LIMIT_SCORE, settings.MAX_LIMIT_SCORE)

    def is_full_limit(self):
        """
        判断代理池是否已满
        :return: 满了则返回True 否则返回False
        """
        if self.get_pool_count() >= POOL_UPPER_LIMIT:
            print('当前代理池已满')
            return True
        else:
            return False


def storer_test():
    rdc = RedisCli()
    print(rdc.get_pool_count())


if __name__ == '__main__':
    storer_test()



