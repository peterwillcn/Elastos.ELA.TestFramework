#!/usr/bin/env python
# -*- coding:utf-8 -*-
# date: 2019/3/28 3:37 PM
# author: liteng

import os
from middle import util
from middle.overall import Overall


class Controller(object):

    def __init__(self):
        self.tag = "[top.control.Controller]"
        self.config = util.read_config_file("./config.json")
        self.middle = Overall(self.config["configuration"])


if __name__ == "__main__":
    c = Controller()
    ret = c.middle.deploy_node()
    if not ret:
        print("deploy node failed!")
