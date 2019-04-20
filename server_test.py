#!/usr/bin/env python
# -*- coding:utf-8 -*-
# date: 2019/4/18 5:48 PM
# author: liteng

from tests.dpos_test import DposTest

from src.middle.tools.log import Logger


if __name__ == '__main__':

    t = DposTest()

    for i in range(10):
        Logger.warn("begin {} times test".format(i))
        t.run()
        Logger.warn("end {} times test".format(i))
