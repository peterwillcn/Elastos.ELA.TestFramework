#!/usr/bin/env python
# -*- coding:utf-8 -*-
# date: 2019/4/5 3:31 PM
# author: liteng

import time

from src.middle.tools import util
from src.middle.tools.log import Logger

from src.bottom.services.rest import REST
from src.bottom.services.rpc import RPC
from src.bottom.services.jar import JarService

from src.bottom.parameters.params import Parameter


class ServiceManager(object):
    def __init__(self, params: Parameter):
        self.tag = util.tag_from_path(__file__, self.__class__.__name__)
        self.rpc = RPC()
        self.rest = REST()
        self.jar_service = JarService(params.root_path)
        self.ela_number = params.ela_params.number

    def wait_rpc_ready(self, content=1, timeout=60):
        time.sleep(3)
        stop_time = time.time() + timeout
        while time.time() <= stop_time:
            result = []
            for i in range(self.ela_number):
                count = self.rpc.get_connection_count()
                Logger.debug('{} wait for rpc service ready, connection count: {}'.format(self.tag, count))
                if count and count >= content:
                    result.append(True)
                else:
                    result.append(False)
                if result.count(True) == self.ela_number:
                    Logger.debug('{} Nodes connect with each other, '
                                 'rpc service is started on success!.'.format(self.tag))
                    return True
                time.sleep(1)
        Logger.error('{} Node can not connect with each other, wait rpc service timed out!')
        return False

    def mining_blocks_ready(self, foundation_address):
        time.sleep(3)
        self.rpc.discrete_mining(101)
        balance = self.rpc.get_balance_by_address(foundation_address)
        Logger.debug("{} foundation address value: {}".format(self.tag, balance))