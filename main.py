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

    time.sleep(2)
    input_keystore = d.key_manager.key_stores[0]
    output_address = d.key_manager.key_stores[9].address
    result = d.ordinary_transaction(input_keystore, [output_address], 10000 * 100000000)
    Logger.info('[Main test] ordinary transaction result: {}'.format(result))
    rpc_port = d.main_nodes[0].rpc_port
    d.rpc.discrete_mining(2)
    balance1 = d.rpc.get_balance_by_address(input_keystore.address)
    balance2 = d.rest.get_balance_by_address(output_address)
    print('balance1 = ', balance1, 'balance2 = ', balance2)
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


def func4():
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

    time.sleep(2)

    """
    测试RPC各接口功能
    """

    info = d.rpc.get_info()
    Logger.info("info: {}".format(info))
    time.sleep(1)

    connections = d.rpc.get_connection_count()
    Logger.info("connections: {}".format(connections))
    time.sleep(1)

    discrete_mining = d.rpc.discrete_mining(10000)
    #Logger.info('discrete minging: {}'.format(discrete_mining))
    time.sleep(1)

    block_count = d.rpc.get_block_count()
    Logger.info('block count: {}'.format(block_count))
    time.sleep(1)

    count2 = d.rest.get_block_height()
    Logger.warn('block count: {}'.format(count2))

    balance = d.rpc.get_balance_by_address(d.key_manager.key_stores[2].address)
    Logger.info("balance: {}".format(balance))
    time.sleep(1)

    balance2 = d.rest.get_balance_by_address(d.key_manager.key_stores[2].address)
    Logger.warn('balance2: {}'.format(balance2))
    unspent_utxos = d.rpc.list_unspent_utxos(d.key_manager.key_stores[2].address)
    Logger.info("unspent utxos: {}".format(unspent_utxos))
    time.sleep(1)

    toggle_mining = d.rpc.toggle_mining(True)
    Logger.info("toggle minning: {}".format(toggle_mining))
    time.sleep(3)

    block_count = d.rpc.get_block_count()
    Logger.info('block count: {}'.format(block_count))
    time.sleep(1)

    best_block_hash = d.rpc.get_best_block_hash()
    Logger.info("best block hash: {}".format(best_block_hash))
    time.sleep(1)

    block = d.rpc.get_block_by_hash(best_block_hash)
    Logger.info('get block by hash: {}'.format(block))
    time.sleep(1)

    height_block = d.rpc.get_block_by_height(block_count)
    Logger.info('get block by height: {}'.format(height_block))
    time.sleep(1)

    block_hash_height = d.rpc.get_block_hash_by_height(block_count)
    Logger.info('get block hash by height: {}'.format(block_hash_height))
    time.sleep(1)

    raw_mempool = d.rpc.get_raw_mempool()
    Logger.info('get block raw mempool: {}'.format(raw_mempool))
    time.sleep(1)

    neighbors = d.rpc.get_neighbors()
    Logger.info('get neighbors: {}'.format(neighbors))
    time.sleep(1)

    node_state = d.rpc.get_node_state()
    Logger.info('get node state: {}'.format(node_state))
    time.sleep(1)

    set_log_level = d.rpc.set_log_level(0)
    Logger.info('set log level: {}'.format(set_log_level))
    time.sleep(5)

    block_count = d.rpc.get_block_count()
    Logger.info('At last block count: {}'.format(block_count))
    d.stop_nodes(node_type)


if __name__ == "__main__":
    func4()


