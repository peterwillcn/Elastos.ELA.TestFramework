#!/usr/bin/env python
# encoding: utf-8

# author: liteng
# contact: liteng0313@gmail.com
# time: 2019-01-16 19:07
# file: log.py

import time


class Logger:

    level = 0
    COLOR_END = "\033[0m"
    COLOR_BLUE = "\033[0;34m"
    COLOR_GREEN = "\033[1;32m"
    COLOR_YELLOW = "\033[1;33m"
    COLOR_RED = "\033[0;31m"

    @staticmethod
    def debug(msg):
        if Logger.level == 0:
            current_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
            print(current_time + Logger.COLOR_BLUE + " [DEBUG] " + Logger.COLOR_END + msg)

    @staticmethod
    def info(msg):
        if Logger.level <= 1:
            current_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
            print(current_time + Logger.COLOR_GREEN + " [INFO] " + Logger.COLOR_END + msg)

    @staticmethod
    def warn(msg):
        if Logger.level <= 2:
            current_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
            print(current_time + Logger.COLOR_YELLOW + " [WARN] " + Logger.COLOR_END + msg)

    @staticmethod
    def error(msg):
        if Logger.level <= 3:
            current_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
            print(current_time + Logger.COLOR_RED + " [ERROR] " + Logger.COLOR_END + msg)


