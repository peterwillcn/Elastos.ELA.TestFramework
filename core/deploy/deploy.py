#!/usr/bin/env python
# -*- coding:utf-8 -*-
# date: 2019/1/20 3:37 PM
# author: liteng

import os
import json
import time
import shutil

from configs import constant
from configs import config
from logs.log import Logger
from core.deploy import node
from core.service import rpc


class Deploy(object):

    def __init__(self):
        self.main_nodes = []
        self.arbiter_nodes = []
        self.did_nodes = []
        self.token_nodes = []
        self.neo_nodes = []
        self.rpc = rpc.RPC()
        self.tag = '[Deploy] '
        self.switch_list = self._switch_list()
        self.switch_path = self._switch_path()
        self.switch_config = self._switch_config()

    def _switch_list(self):
        switcher = {
            constant.NODE_TYPE_MAIN: self.main_nodes,
            constant.NODE_TYPE_ARBITER: self.arbiter_nodes,
            constant.NODE_TYPE_DID: self.did_nodes,
            constant.NODE_TYPE_TOKEN: self.token_nodes,
            constant.NODE_TYPE_NEO: self.neo_nodes
        }
        return switcher

    def _switch_node(self, index, data_dir, _config):
        switcher = {
            constant.NODE_TYPE_MAIN: node.MainNode(index, data_dir, _config),
            # constant.NODE_TYPE_ARBITER: node.ArbiterNode(index, data_dir, _config),
            # constant.NODE_TYPE_DID: node.DidNode(index, data_dir, _config),
            # constant.NODE_TYPE_TOKEN: node.TokenNode(index, data_dir, _config),
            # constant.NODE_TYPE_NEO: node.NeoNode(index, data_dir, _config)
        }
        return switcher

    def _switch_path(self):
        switcher = {
            constant.NODE_TYPE_MAIN: constant.NODE_PATH_MAIN,
            constant.NODE_TYPE_ARBITER: constant.NODE_PATH_ARBITER,
            constant.NODE_TYPE_DID: constant.NODE_PATH_DID,
            constant.NODE_TYPE_TOKEN: constant.NODE_PATH_TOKEN,
            constant.NODE_TYPE_NEO: constant.NODE_PATH_NEO
        }
        return switcher

    def _switch_config(self):
        switcher = {
            constant.NODE_TYPE_MAIN: config.main_chain,
            constant.NODE_TYPE_ARBITER: config.arbiter_chain,
            constant.NODE_TYPE_DID: config.did_chain,
            constant.NODE_TYPE_TOKEN: config.token_chain,
            constant.NODE_TYPE_NEO: config.neo_chain
        }
        return switcher

    def deploy_node_environment(self, node_type: str, num: int):

        if num < 0:
            Logger.error('{} Invalid param num: {}'.format(self.tag, num))
            return False
        Logger.debug('{} deploy {} binary'.format(self.tag, node_type))
        src_path = os.path.join(self.switch_path[node_type])
        if not os.path.exists(src_path):
            Logger.error('{} path not found: '.format(src_path))
            return False
        _config = self.switch_config[node_type]

        for i in range(num):
            dest_path = os.path.join(constant.TEST_PARAENT_PATH, node_type,
                                     constant.CURRENT_DATE_TIME, 'node' + str(i))
            if not os.path.exists(dest_path):
                os.makedirs(dest_path)
            shutil.copy(src_path, dest_path + '/ela')

            config_path = dest_path + '/config.json'
            n = self._switch_node(i, dest_path, _config)[node_type]
            n.reset_config()
            with open(config_path, 'w') as f:
                json.dump(n.config, f, indent=4)
            self.switch_list[node_type].append(n)

        return True

    def start_nodes(self, node_type: str):
        length = len(self.switch_list[node_type])
        for i in range(length):
            self.switch_list[node_type][i].start()
            time.sleep(1)

    def stop_nodes(self, node_type: str):
        length = len(self.switch_list[node_type])
        for i in range(length):
            self.switch_list[node_type][i].stop()

    def wait_rpc_service(self, content=1,  timeout=60):

        stop_time = time.time() + timeout

        while time.time() <= stop_time:
            result = []
            for i in range(len(self.main_nodes)):
                count = self.rpc.get_connection_count(self.main_nodes[i].rpc_port)
                Logger.debug('{} connection count: {}'.format(self.tag, count))
                if count and count >= content:
                    result.append(True)
                else:
                    result.append(False)
                if result.count(True) == len(self.main_nodes):
                    Logger.debug('{} Nodes connect with each other, '
                                 'rpc service is successfully started.'.format(self.tag))
                    return True
                time.sleep(2)
        Logger.error('{} Node can not connect with each other, wait rpc service timed out!')
        return False

    def mining_101_blocks(self):
        hash_list = self.rpc.discrete_mining(self.main_nodes[0].rpc_port, 101)
        if len(hash_list) != 101:
            Logger.error("{} Discrete mining 101 blocks failed.".format(self.tag))
            return False
        Logger.debug('{} Discrete mining 101 blocks on success'.format(self.tag))
        Logger.debug('{} Discrete mining 101 blocks hashes: {}'.format(self.tag, hash_list))
        return True
