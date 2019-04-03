#!/usr/bin/env python
# -*- coding:utf-8 -*-
# date: 2019/4/3 6:20 PM
# author: liteng

import time
from src.top.control import Controller


def vote_normal_test():
    controller = Controller()
    time.sleep(10)
    controller.terminate_all_process()


if __name__ == "__main__":
    vote_normal_test()