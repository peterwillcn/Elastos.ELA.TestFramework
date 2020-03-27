#!/usr/bin/env python
# encoding: utf-8

# author: liteng
# contact: liteng0313@gmail.com
# time: 2019-01-16 19:07
# file: log.py

import pathlib
import time
import logging
import sys
import os


def remove_file():
    script_dir = os.path.abspath("")
    files = sorted(list(pathlib.Path(script_dir).glob("*.log")), reverse=True)
    for f in files[:10]:
        os.remove(str(f))


remove_file()

console_formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
current_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())

# enable logs universally (including for other libraries)
logger = logging.getLogger("TestFramework")
logger.setLevel(logging.DEBUG)

# log to stderr; by default only WARNING and higher
console_stderr_handler = logging.StreamHandler(sys.stderr)
console_stderr_handler.setFormatter(console_formatter)
console_stderr_handler.setLevel(logging.DEBUG)

file_handler = logging.FileHandler(current_time + ".log")
file_handler.setFormatter(console_formatter)
file_handler.setLevel(logging.DEBUG)
logger.addHandler(file_handler)
logger.addHandler(console_stderr_handler)


class Logger(object):
    level = 0
    COLOR_END = "\033[0m"
    COLOR_BLUE = "\033[0;34m"
    COLOR_GREEN = "\033[1;32m"
    COLOR_YELLOW = "\033[1;33m"
    COLOR_RED = "\033[0;31m"

    @staticmethod
    def debug(msg):
        if Logger.level == 0:
            logger.debug(msg)
            # current_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
            # print(current_time + Logger.COLOR_BLUE + " [DEBUG] " + Logger.COLOR_END + msg)

    @staticmethod
    def info(msg):
        if Logger.level <= 1:
            logger.info(msg)

    @staticmethod
    def warn(msg):
        if Logger.level <= 2:
            logger.warn(msg)

    @staticmethod
    def error(msg):
        if Logger.level <= 3:
            logger.error(msg)
