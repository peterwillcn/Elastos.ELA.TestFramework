#!/usr/bin/env python
# encoding: utf-8

# author: liteng
# contact: liteng0313@gmail.com
# time: 2019-01-16 19:07
# file: log.py

import time
from src.middle.tools import constant


class Logger:

    level = 0

    @staticmethod
    def debug(msg):
        if Logger.level == 0:
            current_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
            print(current_time + constant.COLOR_BLUE + " [DEBUG] " + constant.COLOR_END + msg)

    @staticmethod
    def info(msg):
        if Logger.level <= 1:
            current_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
            print(current_time + constant.COLOR_GREEN + " [INFO] " + constant.COLOR_END + msg)

    @staticmethod
    def warn(msg):
        if Logger.level <= 2:
            current_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
            print(current_time + constant.COLOR_YELLOW + " [WARN] " + constant.COLOR_END + msg)

    @staticmethod
    def error(msg):
        if Logger.level <= 3:
            current_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
            print(current_time + constant.COLOR_RED + " [ERROR] " + constant.COLOR_END + msg)

