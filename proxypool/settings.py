# -*- coding: utf-8 -*-

# ---------- Redis Settings Begin ----------
# Redis数据库地址
REDIS_HOST = '127.0.0.1'
# Redis端口
REDIS_PORT = 6379
# Redis密码
REDIS_PWD = None
# ---------- Redis Settings End ----------

VALID_STATUS_CODES = [200]
INITIAL_SCORE = 10
MAX_LIMIT_SCORE = 100
MINI_LIMIT_SCORE = 0

INSPECTOR_MAX_TEXT_COUNT = 10

USER_API_ENABLE = True
USER_API_HOST = '127.0.0.1'
USER_API_PORT = '5000'

INSPECTOR_ENABLE = True
GETTER_ENABLE = True

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36",
}

# class ProxyPoolSettings(object):
#     __instance = None
#
#     def __new__(cls, *args, **kwargs):
#         if cls.__instance == None:
#             cls.__instance = object.__new__(cls)
#         return cls.__instance
#
#     def __init__(self):
#         self.headers = {
#             "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36",
#         }
#         self.max_page = 50
#
#     def get_headers(self):
#         return self.headers

