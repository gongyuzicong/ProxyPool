# -*- coding: utf-8 -*-

from flask import Flask, g
from proxypool import storer

__all__ = ['app']

app = Flask(__name__)


def get_conn():
    if not hasattr(g, 'redis'):
        g.redis = storer.RedisCli()
    return g.redis


@app.route('/')
def index():
    return '<h2>Welcome to Proxy Pool System</h2>' \
           '<h3>You can get the proxy from the api from "/random" or "/count"</h3>'


@app.route('/random')
def get_proxy():
    """
    Get a proxy
    :return: 随机代理
    """
    conn = get_conn()
    return conn.get_proxy_random()


@app.route('/count')
def get_count():
    """
    Get the count of proxies
    :return: 代理池总量
    """
    conn = get_conn()
    return str(conn.get_pool_count())


if __name__ == '__main__':
    app.run()



