# -*- coding: utf-8 -*-
from proxypool import scheduler
import asyncio

def main():
    try:
        s = scheduler.Scheduler()
        s.schedule_start()
    except Exception as e:
        main()


if __name__ == '__main__':
    main()

