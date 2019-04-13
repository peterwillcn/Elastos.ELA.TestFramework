#!/usr/bin/env python
# -*- coding:utf-8 -*-
# date: 2019/3/28 3:37 PM
# author: liteng

import os
import time


from src.middle.tools import util
from src.middle.tools.log import Logger
from src.middle.distribute import Distribution


class Controller(object):

    def __init__(self, up_config: dict):
        self.tag = util.tag_from_path(__file__, self.__class__.__name__)
        self.root_path = os.path.abspath(os.path.join(os.path.abspath(__file__), "../../.."))
        print(self.root_path)
        self.config = util.read_config_file(os.path.join(self.root_path, "config.json"))
        self.up_config = up_config
        self.node_types = ["ela", "arbiter", "did", "token", "neo"]
        self.reset_config(self.up_config)
        self.middle = Distribution(self.config, self.root_path)
        # self.middle.init_for_testing()

    def discrete_mining_blocks(self, num: int):
        self.middle.service_manager.rpc.discrete_mining(num)

    def get_current_height(self):
        return self.middle.service_manager.rpc.get_block_count()

    def loop_for_ever(self):
        while True:
            current_height = self.get_current_height()
            Logger.info("[main] current height: {}".format(current_height))
            self.discrete_mining_blocks(1)
            time.sleep(2)

    def terminate_all_process(self):
        Logger.info("{} terminal all the process and exit...".format(self.tag))
        self.middle.service_manager.jar_service.stop()
        self.middle.node_manager.stop_nodes()
        exit(-1)

    def reset_config(self, up_config: dict):
        for key in up_config.keys():
            if key is "side":
                if not up_config[key]:
                    self.forbidden_side_chain()
                continue

            if key in self.node_types:
                self.reset_sub_config(key)

    def reset_sub_config(self, key: str):
        _config = self.up_config[key]
        for k in _config.keys():
            self.config[key][k] = _config[k]

    def forbidden_side_chain(self):
        self.config["arbiter"]["enable"] = False
        self.config["did"]["enable"] = False
        self.config["token"]["enable"] = False
        self.config["neo"]["enable"] = False

    def test_result(self, case: str, result: bool):
        current_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        if result:
            print(current_time + Logger.COLOR_GREEN + " [PASS!] " + Logger.COLOR_END + case)
        else:
            print(current_time + Logger.COLOR_RED + " [NOT PASS!] " + Logger.COLOR_END + case)
            self.terminate_all_process()

    def get_tap_keystore(self):
        return self.middle.keystore_manager.special_key_stores[4]

    def get_register_nickname_public_key(self):
        public_key_nickname = dict()
        for i in range(self.middle.params.ela_params.crc_number):
            public_key_nickname[self.middle.keystore_manager.node_key_stores[i].public_key.hex()] = "Crc-" + str(i)
        list_producers = self.middle.service_manager.rpc.list_producers(0, 100)
        print(list_producers)
        for producer in list_producers["producers"]:
            public_key_nickname[producer["nodepublickey"]] = producer["nickname"]
        Logger.debug("{} node_publickey -> nickname: {}".format(self.tag, public_key_nickname))
        return public_key_nickname

    def get_current_arbiter_nicknames(self):
        public_key_nickname = self.get_register_nickname_public_key()
        arbiters = self.middle.service_manager.rpc.get_arbiters_info()["arbiters"]
        current_nicknames = list()
        for public_key in arbiters:
            current_nicknames.append(public_key_nickname[public_key])

        return current_nicknames
