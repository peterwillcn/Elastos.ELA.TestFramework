#!/usr/bin/env python
# encoding: utf-8

# author: liteng
# contact: liteng0313@gmail.com
# time: 2019-01-16 19:07
# file: log.py

import time
from middle import constant


class Logger:

    level = 0

    @staticmethod
    def debug(msg):
        if Logger.level == 0:
            current_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
            print(constant.COLOR_BLUE + current_time + "[DEBUG] " + msg + constant.COLOR_END)

    @staticmethod
    def info(msg):
        if Logger.level <= 1:
            current_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
            print(constant.COLOR_GREEN + current_time + "[INFO] " + msg + constant.COLOR_END)

    @staticmethod
    def warn(msg):
        if Logger.level <= 2:
            current_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
            print(constant.COLOR_YELLOW + current_time + "[WARN] " + msg + constant.COLOR_END)

    @staticmethod
    def error(msg):
        if Logger.level <= 3:
            current_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
            print(constant.COLOR_RED + current_time + "[ERROR] " + msg + constant.COLOR_END)

