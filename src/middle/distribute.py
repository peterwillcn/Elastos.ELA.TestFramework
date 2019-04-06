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
        self.service_manager = ServiceManager(self.params)
        self.keystore_manager = KeyStoreManager(self.params)
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
        self.init_for_testing()

    def init_for_testing(self):
        self.node_manager.deploy_nodes()
        self.node_manager.start_nodes()
        self.service_manager.wait_rpc_ready()
        self.service_manager.mining_blocks_ready(self.node_manager.foundation_address)
        self.tx_manager.recharge_tap_wallet(20000000 * constant.TO_SELA)
        self.tx_manager.recharge_producer_wallet(10000 * constant.TO_SELA)
        self.tx_manager.register_producers_candidates()
        self.tx_manager.vote_producers_candidates()

    def check_params(self):
        if self.params.ela_params.number < 3 * self.params.ela_params.crc_number:
            Logger.error("{} ela node number should be >= 3 * crc number, please check your config.json, exit...")
            time.sleep(1)
            exit(-1)



