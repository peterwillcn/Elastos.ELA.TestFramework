#!/usr/bin/env python
# -*- coding:utf-8 -*-
# date: 2019/1/20 3:37 PM
# author: liteng

import os
import json
import shutil
from configs import constant
from configs import config
from logs.log import Logger
from core.deploy import node


class Deploy(object):

    def __init__(self):
        self.main_nodes = []
        self.arbiter_nodes = []
        self.did_nodes = []
        self.token_nodes = []
        self.neo_nodes = []
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

    def _switch_node(self, _config):
        switcher = {
            constant.NODE_TYPE_MAIN: node.MainNode(_config),
            constant.NODE_TYPE_ARBITER: node.ArbiterNode(_config),
            constant.NODE_TYPE_DID: node.DidNode(_config),
            constant.NODE_TYPE_TOKEN: node.TokenNode(_config),
            constant.NODE_TYPE_NEO: node.NeoNode(_config)
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
            shutil.copy(src_path, dest_path)

            config_path = dest_path + '/config.json'
            n = self._switch_node(_config)[node_type]
            n.reset_config(i)
            with open(config_path, 'w') as f:
                json.dump(n.config, f, indent=4)
            self.switch_list[node_type].append(node)

        return True
