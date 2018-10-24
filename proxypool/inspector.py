# -*- coding: utf-8 -*-

from proxypool import storer
import aiohttp
import asyncio
from proxypool import settings
import time

URL = 'http://www.baidu.com'


class Inspector(object):
    def __init__(self):
        self.redis = storer.RedisCli()

    async def test_single_proxy(self, proxy):
        try:
            connect = aiohttp.TCPConnector(verify_ssl=False)
            async with aiohttp.ClientSession(connector=connect, headers=settings.HEADERS) as session:

                if isinstance(proxy, bytes):
                    proxy = proxy.decode('utf-8')
                proxy_str = 'http://' + proxy
                print('正在测试代理: {}'.format(proxy))
                async with session.get(URL, proxy=proxy_str, timeout=15) as response:
                    if response.status in settings.VALID_STATUS_CODES:
                        self.redis.set_proxy_max_score(proxy)
                    else:
                        self.redis.dec_proxy_score(proxy)
        except (aiohttp.ClientError, aiohttp.ClientConnectorError,
                asyncio.TimeoutError, AttributeError):
            print('代理请求失败: {}'.format(proxy))
            self.redis.dec_proxy_score(proxy)
        except Exception as e:
            print("其他错误: ", e.args)

    def start(self):
        print('开始测试检测模块...')
        try:
            proxies = self.redis.get_all_proxy()
            event_loop = asyncio.get_event_loop()
            print('当前测试{}个代理...'.format(len(proxies)))
            for index in range(0, len(proxies), settings.INSPECTOR_MAX_TEXT_COUNT):
                print('正在测试第{}-{}个代理...'.format(index + 1, index+settings.INSPECTOR_MAX_TEXT_COUNT))
                test_proxies = proxies[index: index+settings.INSPECTOR_MAX_TEXT_COUNT]
                tasks_list = [self.test_single_proxy(proxy) for proxy in test_proxies]
                event_loop.run_until_complete(asyncio.wait(tasks_list))
                time.sleep(5)
        except Exception as e:
            print("Error in Inspector: ", e.args)


def inspector_test():
    ins = Inspector()
    ins.start()


if __name__ == '__main__':
    inspector_test()
