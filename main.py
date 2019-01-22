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
from configs import constant
from core.deploy import deploy
from core.wallet import keystore
from core.wallet import keystoremanager


def func1():
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
    d.check_foundation_amount()
    result = d.mining_101_blocks()
    if result:
        Logger.info('[Main test] Discrete mining 101 blocks on success.')
    time.sleep(10)
    d.stop_nodes(node_type)


def func2():
    k = keystoremanager.KeyStoreManager(10)
    time.sleep(1)
    print('length: ', len(k.key_stores))


def func3():
    d = deploy.Deploy()
    result = d.deploy_node_environment(constant.NODE_TYPE_MAIN, 4)
    Logger.info('[Main test] result = {}'.format(result))

    result = d.deploy_node_environment(constant.NODE_TYPE_ARBITER, 4)
    Logger.info('[Main test] deploy {} result: {}'.format(constant.NODE_TYPE_ARBITER, result))

    result = d.deploy_node_environment(constant.NODE_TYPE_DID, 4)
    Logger.info('[Main test] deploy {} result: {}'.format(constant.NODE_TYPE_DID, result))

    result = d.deploy_node_environment(constant.NODE_TYPE_TOKEN, 4)
    Logger.info('[Main test] deploy {} result: {}'.format(constant.NODE_TYPE_TOKEN, result))

    result = d.deploy_node_environment(constant.NODE_TYPE_NEO, 4)
    Logger.info('[Main test] deploy {} result: {}'.format(constant.NODE_TYPE_NEO, result))


if __name__ == "__main__":
    func3()


