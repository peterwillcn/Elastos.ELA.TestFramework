#!/usr/bin/env python
# -*- coding:utf-8 -*-
# date: 2019/3/28 2:48 PM
# author: liteng

import time

from src.tools import util, constant
from src.tools.log import Logger
from src.core.parameters.params import Parameter

from src.core.managers.env_manager import EnvManager
from src.core.managers.node_manager import NodeManager
from src.core.managers.service_manager import ServiceManager
from src.core.managers.keystore_manager import KeyStoreManager
from src.core.managers.tx_manager import TransactionManager


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

    def ready_for_dpos(self):
        self.tx_manager.register_producers_candidates()
        Logger.info("{} register producer on success!".format(self.tag))
        self.tx_manager.vote_producers_candidates()
        Logger.info("{} vote producer on success!".format(self.tag))




