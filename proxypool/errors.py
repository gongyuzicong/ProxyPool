# -*- coding: utf-8 -*-


class ProxyEmptyErrors(Exception):
    def __init__(self):
        Exception.__init__(self)

    def __str__(self):
        print('代理池资源为空')