#!/usr/bin/env python
# -*- coding:utf-8 -*-
# date: 2019/4/18 3:55 PM
# author: liteng

import time

from datetime import datetime

from src.top.control import Controller

from src.middle.tools import util
from src.middle.tools.log import Logger


class DposTest(object):

    def __init__(self):
        self.tag = util.tag_from_path(__file__, self.__class__.__name__)
        self.config = {
            "ela": {
                "enable": True,
                "password": "123",
                "number": 16,
                "crc_number": 4,
                "pre_connect_offset": 5,
                "crc_dpos_height": 200,
                "public_dpos_height": 220
            },
            "side": False,
            "stop": True,
            "times": 1
        }
        self.controller = None
        self.number = self.config["ela"]["number"]
        self.crc_number = self.config["ela"]["crc_number"]
        self.h1 = self.config["ela"]["crc_dpos_height"]
        self.h2 = self.config["ela"]["public_dpos_height"]

    def run(self):
        self.before_test()
        self.normal_test()
        self.minor_stop_test()
        self.after_test()

    def before_test(self):
        self.controller = Controller(self.config)
        self.controller.middle.ready_for_dpos()

    def normal_test(self):
        time1 = datetime.now()
        while True:
            time2 = datetime.now()
            diff = (time2 - time1).seconds
            Logger.debug("{} current diff: {} seconds".format(self.tag, diff))
            if diff >= 5 * 60:
                result = False
                break
            current_height = self.controller.get_current_height()
            Logger.debug("{} current height: {}".format(self.tag, current_height))
            num = self.h1 - current_height
            if num > 0:
                self.controller.discrete_mining_blocks(num)
            else:
                self.controller.discrete_mining_blocks(1)
            time.sleep(1)

            if current_height == self.h1 + 1:
                Logger.info("{} H1 PASS!".format(self.tag))
                Logger.info("{} H1 PASS!".format(self.tag))

            if current_height == self.h2 + 2:
                Logger.info("{} H2 PASS!".format(self.tag))
                Logger.info("{} H2 PASS!".format(self.tag))

            if current_height >= self.h2 + self.crc_number * 3 * 1:
                result = True
                break

        self.controller.test_result("dpos normal test", result)

    def minor_stop_test(self):
        current_height = self.controller.get_current_height()
        if current_height < self.h2:
            return False

        inactive_nodes = self.controller.middle.node_manager.ela_nodes[self.crc_number + 1: self.crc_number * 2]
        candidate_nodes = self.controller.middle.node_manager.ela_nodes[self.crc_number * 3 + 1: self.crc_number * 4]

        index = 0
        stop_height = self.h2 + 12
        if current_height < stop_height:
            num = stop_height - current_height
            for i in range(num):
                self.controller.discrete_mining_blocks(1)
                time.sleep(1)
                self.controller.show_current_height()

        inactive_nodes[index].stop()

        stop_height = self.controller.get_current_height() + self.crc_number * 3 * 1
        current_height = self.controller.get_current_height()
        time1 = datetime.now()

        test_case = "one node stops continue consensus"

        while current_height <= stop_height:
            time2 = datetime.now()
            diff = (time2 - time1).seconds
            Logger.debug("{} diff: {} seconds".format(self.tag, diff))
            if diff >= 2 * 60:
                self.controller.test_result(test_case, False)
            self.controller.discrete_mining_blocks(1)
            current_height = self.controller.get_current_height()
            self.controller.show_current_height()
            time.sleep(1)

        self.controller.test_result(test_case, True)

        index += 1
        test_case = "two nodes stop continue consensus"
        inactive_nodes[index].stop()
        stop_height = self.controller.get_current_height() + self.crc_number * 3 * 1
        time1 = datetime.now()
        while current_height <= stop_height:
            time2 = datetime.now()
            diff = (time2 - time1).seconds
            Logger.debug("{} diff: {} seconds".format(self.tag, diff))
            if diff >= 2 * 60:
                self.controller.test_result(test_case, False)
            self.controller.discrete_mining_blocks(1)
            current_height = self.controller.get_current_height()
            self.controller.show_current_height()
            time.sleep(1)
        self.controller.test_result(test_case, True)

        index += 1
        test_case = "three nodes stop continue consensus"
        inactive_nodes[index].stop()
        stop_height = self.controller.get_current_height() + self.crc_number * 3 * 1
        time1 = datetime.now()
        while current_height <= stop_height:
            time2 = datetime.now()
            diff = (time2 - time1).seconds
            Logger.debug("{} diff: {} seconds".format(self.tag, diff))
            if diff >= 2 * 60:
                self.controller.test_result(test_case, False)
            self.controller.discrete_mining_blocks(1)
            current_height = self.controller.get_current_height()
            self.controller.show_current_height()
            time.sleep(1)
        self.controller.test_result(test_case, True)

    def after_test(self):
        self.controller.terminate_all_process()

