#!/usr/bin/env python
# -*- coding:utf-8 -*-
# date: 2019/3/28 2:48 PM
# author: liteng

import time

from src.middle.tools import util
from src.middle.tools import constant
from src.middle.tools.log import Logger
from src.bottom.parameters.params import Parameter

from src.middle.managers.env_manager import EnvManager
from src.middle.managers.node_manager import NodeManager
from src.middle.managers.service_manager import ServiceManager
from src.middle.managers.keystore_manager import KeyStoreManager
from src.middle.managers.transaction_manager import TransactionManager


class Distribution(object):

    def __init__(self, top_config, root_path: str):
        self.tag = util.tag_from_path(__file__, self.__class__.__name__)
        self.params = Parameter(top_config, root_path)
        self.check_params()
        self.env_manager = EnvManager()
        self.keystore_manager = KeyStoreManager(self.params)
        self.service_manager = ServiceManager(self.params)
        self.step = 0

        self.node_manager = NodeManager(
            self.params,
            self.env_manager,
            self.service_manager,
            self.keystore_manager
        )
        self.tx_manager = TransactionManager(
            self.params,
            self.node_manager
        )

    def init_for_testing(self):
        self.node_manager.deploy_nodes()
        Logger.info("{} deploying nodes on success!".format(self.tag))
        self.node_manager.start_nodes()
        Logger.info("{} starting nodes on success!".format(self.tag))
        self.service_manager.mining_blocks_ready(self.node_manager.main_foundation_address)
        Logger.info("{} mining 101 blocks on success!".format(self.tag))
        time.sleep(5)
        self.tx_manager.recharge_tap_keystore(20000000 * constant.TO_SELA)
        Logger.info("{} recharge tap keystore {} ELAs on success!".format(self.tag, 20000000 * constant.TO_SELA))
        if self.params.arbiter_params.enable:
            self.tx_manager.recharge_arbiter_keystore(3 * constant.TO_SELA)
            Logger.info("{} recharge each arbiter keystore {} ELAs on success!")
            self.tx_manager.recharge_sub_keystore(3 * constant.TO_SELA)
            Logger.info("{} recharge each sub keystore {} ELAs on success!")
        self.tx_manager.recharge_producer_keystore(10000 * constant.TO_SELA)

    def ready_for_dpos(self):
        Logger.info("{} recharge producer on success!".format(self.tag))
        self.tx_manager.register_producers_candidates()
        Logger.info("{} register producer on success!".format(self.tag))
        self.tx_manager.vote_producers_candidates()
        Logger.info("{} vote producer on success!".format(self.tag))

    def check_params(self):
        if self.params.ela_params.number < 3 * self.params.ela_params.crc_number:
            Logger.error("{} ela node number should be >= 3 * crc number, please check your config.json, exit...")
            time.sleep(1)
            exit(-1)

        # if self.params.arbiter_params.enable and \
        #         self.params.arbiter_params.number != (5 + self.params.ela_params.crc_number):
        #     Logger.error("{} arbiter number should be == 5 + crc number, please check your config.json, exit...")
        #     time.sleep(1)
        #     exit(-1)



