#!/usr/bin/env python
# encoding: utf-8

# author: liteng
# contact: liteng0313@gmail.com
# time: 2019-01-16 18:00
# file: main.py

import os
import time
import shutil
from configs import config
from logs.log import Logger
from core.deploy import deploy
from configs import constant

if __name__ == "__main__":

    Logger.level = 0
    d = deploy.Deploy()
    node_type = constant.NODE_TYPE_MAIN
    result = d.deploy_node_environment(constant.NODE_TYPE_MAIN, 4)
    if result:
        Logger.info('[Main test] Deploy {} on success'.format(node_type))

    time.sleep(1)
    d.start_nodes(node_type)
    Logger.info('[Main test] Start {} on success'.format(node_type))
    result = d.wait_rpc_service()
    if result:
        Logger.info('[Main test] Wait rpc service on success')
    time.sleep(3)
    result = d.mining_101_blocks()
    if result:
        Logger.info('[Main test] Discrete mining 101 blocks on success.')
    time.sleep(10)
    d.stop_nodes(node_type)

