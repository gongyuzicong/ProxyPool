# -*- coding:utf-8 -*-
import time
from proxypool import inspector
from proxypool import getter
from proxypool import user_api
from proxypool import settings
from multiprocessing import Process
import asyncio
import gevent


INSPECTOR_CYCLE = 120
GETTER_CYCLE = 360


class Scheduler(object):
    def schedule_inspector(self, cycle=INSPECTOR_CYCLE):
        ins = inspector.Inspector()
        while True:
            print('检测器开始运行...')
            ins.start()
            time.sleep(cycle)

    def schedule_getter(self, cycle=GETTER_CYCLE):
        get = getter.Getter()
        while True:
            print('获取器开始运行...')
            get.start()
            time.sleep(cycle)

    def schedule_user_api(self):
        print('用户接口开始运行...')
        user_api.app.run(settings.USER_API_HOST, settings.USER_API_PORT)

    def schedule_start(self):
        print('调度器开始运行...')
        if settings.GETTER_ENABLE:
            getter_process = Process(target=self.schedule_getter)
            getter_process.start()

        if settings.INSPECTOR_ENABLE:
            inspector_process = Process(target=self.schedule_inspector)
            inspector_process.start()

        if settings.USER_API_ENABLE:
            user_api_process = Process(target=self.schedule_user_api)
            user_api_process.start()
