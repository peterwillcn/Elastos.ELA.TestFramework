#!/usr/bin/env python
# -*- coding:utf-8 -*-
# date: 2019/5/7 7:05 PM
# author: liteng

import os
import time

from src.core.services import rpc
from src.core.parameters.params import Parameter
from src.core.managers.env_manager import EnvManager
from src.core.managers.node_manager import NodeManager
from src.core.managers.keystore_manager import KeyStoreManager
from src.core.managers.tx_manager import TransactionManager
from src.tools import util
from src.tools import constant
from src.tools.log import Logger


class Controller(object):

    def __init__(self, up_config: dict):
        self.tag = util.tag_from_path(__file__, Controller.__name__)

        # set config
        self.up_config = up_config
        self.root_path = os.path.abspath(os.path.join(os.path.abspath(__file__), "../../"))
        self.config = util.read_config_file(os.path.join(self.root_path, "config.json"))
        self.node_types = ["ela", "arbiter", "did", "token", "neo"]
        self.reset_config(up_config)

        self.params = Parameter(self.config, self.root_path)
        self.check_params()
        self.env_manager = EnvManager()
        self.keystore_manager = KeyStoreManager(self.params)

        self.node_manager = NodeManager(self.params, self.env_manager, self.keystore_manager)
        self.tx_manager = TransactionManager(self.params, self.node_manager)

        # init tap amount and register amount(unit: ELA)
        self.tap_amount = 20000000
        self.register_amount = 10000

        # necessary keystore
        self.foundation_keystore = self.keystore_manager.special_key_stores[0]
        self.tap_keystore = self.keystore_manager.special_key_stores[4]

        self.init_for_testing()

    def init_for_testing(self):
        self.node_manager.deploy_nodes()
        Logger.info("{} deploying nodes on success!".format(self.tag))
        self.node_manager.start_nodes()
        Logger.info("{} starting nodes on success!".format(self.tag))
        self.mining_blocks_ready(self.node_manager.main_foundation_address)
        Logger.info("{} mining 110 blocks on success!".format(self.tag))
        time.sleep(5)

        ret = self.tx_manager.recharge_necessary_keystore(
            input_keystore=self.foundation_keystore,
            keystores=[self.tap_keystore],
            amount=self.tap_amount * constant.TO_SELA
        )

        self.check_result("recharge tap keystore", ret)

        Logger.info("{} recharge tap keystore {} ELAs on success!".format(self.tag, self.tap_amount * constant.TO_SELA))

        ret = self.tx_manager.recharge_necessary_keystore(
            input_keystore=self.tap_keystore,
            keystores=self.keystore_manager.owner_key_stores,
            amount=self.register_amount * constant.TO_SELA
        )

        self.check_result("recharge owner keystore", ret)

        Logger.info("{} recharge producer on success!".format(self.tag))

        if self.params.arbiter_params.enable:
            ret = self.tx_manager.recharge_necessary_keystore(
                input_keystore=self.tap_keystore,
                keystores=self.keystore_manager.arbiter_stores,
                amount=3 * constant.TO_SELA
            )

            self.check_result("recharge arbiter keystore", ret)
            Logger.info("{} recharge each arbiter keystore {} ELAs on success!")

            ret = self.tx_manager.recharge_necessary_keystore(
                input_keystore=self.tap_keystore,
                keystores=self.keystore_manager.sub_key_stores,
                amount=3 * constant.TO_SELA
            )
            self.check_result("recharge sub keystore", ret)
            Logger.info("{} recharge each sub keystore {} ELAs on success!")

            ret = self.tx_manager.recharge_necessary_keystore(
                input_keystore=self.tap_keystore,
                keystores=self.keystore_manager.sub_key_stores2,
                amount=3 * constant.TO_SELA
            )
            self.check_result("recharge sub keystore2", ret)
            Logger.info("{} recharge each sub keystore2 {} ELAs on success!")

    def check_result(self, what: str, result: bool):
        if not result:
            Logger.error("{} failed".format(what))
            self.terminate_all_process()
            return

    def ready_for_dpos(self):
        self.tx_manager.register_producers_candidates()
        Logger.info("{} register producer on success!".format(self.tag))
        self.tx_manager.vote_producers_candidates()
        Logger.info("{} vote producer on success!".format(self.tag))

    def check_params(self):
        if self.params.ela_params.number < 3 * self.params.ela_params.crc_number + \
                self.params.ela_params.later_start_number:
            Logger.error("Ela node number should be >= 3 * crc number + later start number , " 
                         "please check your config in the beginning of your test case or config.json, exit...")
            time.sleep(1)
            exit(-1)

    def reset_config(self, up_config: dict):
        for key in up_config.keys():
            if key is "side":
                if not up_config[key]:
                    self.config["arbiter"]["enable"] = False
                    self.config["did"]["enable"] = False
                    self.config["token"]["enable"] = False
                    self.config["neo"]["enable"] = False
                continue

            if key in self.node_types:
                _config = self.up_config[key]
                for k in _config.keys():
                    self.config[key][k] = _config[k]

    def mining_blocks_ready(self, foundation_address):
        time.sleep(3)
        rpc.discrete_mining(110)
        balance = rpc.get_balance_by_address(foundation_address)
        Logger.debug("{} foundation address value: {}".format(self.tag, balance))

    @staticmethod
    def get_current_height():
        return rpc.get_block_count()

    @staticmethod
    def discrete_mining_blocks(num: int):
        rpc.discrete_mining(num)

    @staticmethod
    def get_height_times(height_times: dict, current_height: int):
        if current_height not in height_times.keys():
            height_times[current_height] = 1
        else:
            height_times[current_height] += 1
        return height_times[current_height]

    @staticmethod
    def get_producer_state(index: int):
        list_producers = rpc.list_producers(0, 100)
        producers = list_producers["producers"]
        return producers[index]["state"]

    def get_register_nickname_public_key(self):
        public_key_nickname = dict()
        for i in range(self.params.ela_params.crc_number + 1):
            if i == 0:
                continue
            public_key_nickname[self.keystore_manager.node_key_stores[i].public_key.hex()] = \
                "CRC-{:0>3d}".format(i)
        list_producers = rpc.list_producers(0, 100)
        for producer in list_producers["producers"]:
            public_key_nickname[producer["nodepublickey"]] = producer["nickname"]
        # Logger.debug("{} node_publickey -> nickname: {}".format(self.tag, public_key_nickname))
        return public_key_nickname

    def get_current_arbiter_nicknames(self):
        public_key_nickname = self.get_register_nickname_public_key()
        arbiters = rpc.get_arbiters_info()["arbiters"]
        current_nicknames = list()
        for public_key in arbiters:
            current_nicknames.append(public_key_nickname[public_key])

        return current_nicknames

    def get_next_arbiter_nicknames(self):
        public_key_nickname = self.get_register_nickname_public_key()
        # print(public_key_nickname)
        arbiters = rpc.get_arbiters_info()["nextarbiters"]
        # print(arbiters)
        current_nicknames = list()
        for public_key in arbiters:
            current_nicknames.append(public_key_nickname[public_key])

        return current_nicknames

    def show_current_height(self):
        current_height = self.get_current_height()
        Logger.debug("{} current height: {}".format(self.tag, current_height))

    @staticmethod
    def get_list_producers_nicknames():
        list_producers = rpc.list_producers(0, 100)
        producers = list_producers["producers"]
        producers_nickname = list()
        for producer in producers:
            producers_nickname.append(producer["nickname"])
        return producers_nickname

    @staticmethod
    def get_current_arbiter_public_keys():
        return rpc.get_arbiters_info()["arbiters"]

    def show_current_next_info(self):
        arbiters_nicknames = self.get_current_arbiter_nicknames()
        arbiters_nicknames.sort()
        next_arbiter_nicknames = self.get_next_arbiter_nicknames()
        next_arbiter_nicknames.sort()
        Logger.info("current arbiters nicknames: {}".format(arbiters_nicknames))
        Logger.info("next    arbiters nicknames: {}".format(next_arbiter_nicknames))

    def terminate_all_process(self):
        Logger.info("{} terminal all the process and exit...".format(self.tag))
        self.node_manager.stop_nodes()

    def test_result(self, case: str, result: bool):
        current_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        if result:
            print(current_time + Logger.COLOR_GREEN + " [PASS!] " + Logger.COLOR_END + case + "\n")
        else:
            print(current_time + Logger.COLOR_RED + " [NOT PASS!] " + Logger.COLOR_END + case + "\n")
            self.terminate_all_process()
            exit(0)