#!/usr/bin/env python
# -*- coding:utf-8 -*-
# date: 2019/4/1 3:22 PM
# author: liteng

import time
from top.control import Controller


if __name__ == "__main__":
    controller = Controller()
    time.sleep(60)
    controller.terminate_all_process()
