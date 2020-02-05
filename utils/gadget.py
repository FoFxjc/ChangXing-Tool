#!/usr/bin/env python
# -*- coding: utf-8 -*-

import time


class Timer:
    """
    秒表工具:构造启动后,每次调用get,可以获取自启动开始的运行时间
    启动方法:timer.timer()
    获取运行时间方法:timer.get()
    """
    stamp_start = None

    def __init__(self):
        """
        秒表工具:构造器
        """
        self.stamp_start = time.time()

    def get(self, ms=False):
        """ 秒表工具:获取当前运行时间
        :param ms:是否返回毫秒(默认=False)
        :return:(float)当前的运行时间(单位:秒/毫秒)
        """
        if ms:
            return 1000 * (time.time() - self.stamp_start)
        else:
            return time.time() - self.stamp_start
