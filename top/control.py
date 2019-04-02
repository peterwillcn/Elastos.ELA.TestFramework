#!/usr/bin/env python
# -*- coding:utf-8 -*-
# date: 2019/3/28 3:37 PM
# author: liteng

import os

from middle.common import constant
from middle.common import util
from middle.overall import Overall


class Controller(object):

    def __init__(self):
        self.tag = "[top.control.Controller]"
        self.project_root_path = os.path.abspath(os.path.join(os.path.abspath(__file__), "../../"))
        self.config = util.read_config_file(os.path.join(self.project_root_path, "top/config.json"))
        self.middle = Overall(self.config, self.project_root_path)

        self.middle.deploy_node()
        self.middle.start_node()
        self.middle.recharge_tap_wallet(20000000 * constant.TO_SELA)

    def discrete_mining_blocks(self, num: int):
        self.middle.rpc.discrete_mining(num)

    def terminate_all_process(self):
        self.middle.jar_server.stop()
        self.middle.stop_node()