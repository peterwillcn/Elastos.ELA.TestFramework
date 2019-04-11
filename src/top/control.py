#!/usr/bin/env python
# -*- coding:utf-8 -*-
# date: 2019/3/28 3:37 PM
# author: liteng

import os

from src.middle.tools import util
from src.middle.distribute import Distribution


class Controller(object):

    def __init__(self, up_config: dict):
        self.tag = util.tag_from_path(__file__, self.__class__.__name__)
        self.root_path = os.path.abspath(os.path.join(os.path.abspath(__file__), "../../.."))
        print(self.root_path)
        self.config = util.read_config_file(os.path.join(self.root_path, "config.json"))
        self.reset_config(up_config)
        self.middle = Distribution(self.config, self.root_path)
        self.middle.init_for_testing()

    def discrete_mining_blocks(self, num: int):
        self.middle.service_manager.rpc.discrete_mining(num)

    def get_current_height(self):
        return self.middle.service_manager.rpc.get_block_count()

    def terminate_all_process(self):
        self.middle.service_manager.jar_service.stop()
        self.middle.node_manager.stop_nodes()

    def reset_config(self, up_config: dict):
        for key in up_config.keys():
            if key is "ela":
                _config = up_config["ela"]
                for k in _config.keys():
                    self.config["ela"][k] = _config[k]

            if key is "side":
                if not up_config[key]:
                    self.forbidden_side_chain()

            if key is "arbiter":
                _config = up_config["arbiter"]
                for k in _config.keys():
                    self.config[key][k] = _config[k]

            if key is "did":
                _config = up_config[key]
                for k in _config.keys():
                    self.config[key][k] = _config[k]

    def forbidden_side_chain(self):
        self.config["arbiter"]["enable"] = False
        self.config["did"]["enable"] = False
        self.config["token"]["enable"] = False
        self.config["neo"]["enable"] = False
