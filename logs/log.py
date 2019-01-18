#!/usr/bin/env python
# encoding: utf-8

# author: liteng
# contact: liteng0313@gmail.com
# time: 2019-01-16 19:07
# file: log.py

import time
from configs import config
class Logger:

    level = 0

    @staticmethod
    def debug(msg):
        if Logger.level == 0:
            current_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
            print(config.COLOR_BLUE + current_time + '[DEBUG] ' + msg + config.COLOR_END)

    @staticmethod
    def info(msg):
        if Logger.level <= 1:
            current_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
            print(config.COLOR_GREEN + current_time + '[INFO] ' + msg + config.COLOR_END)

    @staticmethod
    def warn(msg):
        if Logger.level <= 2:
            current_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
            print(config.COLOR_YELLOW + current_time + '[WARN] ' + msg + config.COLOR_END)

    @staticmethod
    def error(msg):
        if Logger.level <= 3:
            current_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
            print(config.COLOR_RED + current_time + '[ERROR] ' + msg + config.COLOR_END)

