#!/usr/bin/env python
# -*- coding:utf-8 -*-
# date: 2019/3/28 4:44 PM
# author: liteng

import os

from src.middle.tools import util
from src.middle.tools import constant


class Node(object):

    def __init__(self, config):
        self.tag = util.tag_from_path(__file__, self.__class__.__name__)
        self.config = config
        self.dev_null = open(os.devnull, 'w')

        self.node_type_dict = {
            "ela": 10,
            "arbiter": 20,
            "did": 30,
            "token": 40,
            "neo": 50
        }

        self.port_type_dict = {
            "info_port": 1,
            "rest_port": 2,
            "ws_port": 3,
            "json_port": 4,
            "node_port": 5,
            "arbiter_node_port": 6
        }
        pass

    def deploy(self):
        pass

    def start(self):
        pass

    def stop(self):
        pass

    def reset_config_common(self, index, node_type: str, num):
        _config = self.config[constant.CONFIG_TITLE]
        _config[constant.CONFIG_SEED_LIST] = []
        for i in range(num):
            if i == 10:
                break
            _config[constant.CONFIG_SEED_LIST].append("127.0.0.1:" + str(self.reset_port(i, node_type, "node_port")))
        _config[constant.CONFIG_PORT_INFO] = self.reset_port(index, node_type, "info_port")
        _config[constant.CONFIG_PORT_REST] = self.reset_port(index, node_type, "rest_port")
        _config[constant.CONFIG_PORT_WS] = self.reset_port(index, node_type, "ws_port")
        _config[constant.CONFIG_PORT_JSON] = self.reset_port(index, node_type, "json_port")
        _config[constant.CONFIG_PORT_NODE] = self.reset_port(index, node_type, "node_port")
        _config[constant.CONFIG_RPC][constant.CONFIG_RPC_USER] = ""
        _config[constant.CONFIG_RPC][constant.CONFIG_RPC_PASS] = ""
        _config[constant.CONFIG_RPC][constant.CONFIG_RPC_WHITE_LIST] = ["0.0.0.0"]

    def reset_port(self, index, node_type: str, port_type: str):
        port = (100 + index) * 100 + self.node_type_dict[node_type] + self.port_type_dict[port_type]
        return port

