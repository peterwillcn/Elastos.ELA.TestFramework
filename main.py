#!/usr/bin/env python
# encoding: utf-8

# author: liteng
# contact: liteng0313@gmail.com
# time: 2019-01-16 18:00
# file: main.py

import os
import shutil
from configs import config
from logs.log import Logger
from core.deploy import deploy
from configs import constant

if __name__ == "__main__":

    d = deploy.Deploy()
    result = d.deploy_node_environment(constant.NODE_TYPE_MAIN, 5)
    Logger.info('[Main test] deploy result: {}'.format(result))
    result = d.deploy_node_environment(constant.NODE_TYPE_ARBITER, 5)
    Logger.info('[Main test] deploy result: {}'.format(result))
