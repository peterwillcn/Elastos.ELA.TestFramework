#!/usr/bin/env python
# -*- coding:utf-8 -*-
# date: 2019/4/18 3:55 PM
# author: liteng

import time

from datetime import datetime

from src.control import Controller
from src.core.services import rpc
from src.tools import util, constant
from src.tools.log import Logger


class DposTest(object):

    def __init__(self):
        self.tag = util.tag_from_path(__file__, self.__class__.__name__)
        self.config = {
            "ela": {
                "enable": True,
                "password": "123",
                "number": 20,
                "crc_number": 4,
                "pre_connect_offset": 5,
                "crc_dpos_height": 250,
                "public_dpos_height": 280,
                "max_inactivate_rounds": 100
            },
            "side": True,
            "arbiter": {
                "enable": True,
                "number": 9,
                "pow_chain": True,
                "print_level": 0
            },
            "did": {
                "enable": True,
                "number": 5,
                "instant_block": True
            },
            "stop": True,
            "times": 1
        }
        self.controller = None
        self.number = self.config["ela"]["number"]
        self.crc_number = self.config["ela"]["crc_number"]
        self.h1 = self.config["ela"]["crc_dpos_height"]
        self.h2 = self.config["ela"]["public_dpos_height"]
        self.tap_keystore = None

    def run(self):
        self.before_test()
        # self.normal_test()
        # self.rotation_onebyone_test()
        # self.rotation_whole_test()
        # self.minor_stop_test()
        self.inactive_single_test()
        self.cross_normal_test()
        self.cross_stop_test()
        self.after_test()

    def before_test(self):
        self.controller = Controller(self.config)
        self.controller.ready_for_dpos()
        self.tap_keystore = self.controller.keystore_manager.tap_key_store

    def normal_test(self):
        test_case = "1、dpos normal test"
        global result
        time1 = datetime.now()
        height_times = dict()
        height_times[self.controller.get_current_height()] = 1
        while True:
            time2 = datetime.now()
            diff = (time2 - time1).seconds
            Logger.debug("{} current diff: {} seconds".format(self.tag, diff))
            if diff >= 5 * 60:
                result = False
                break
            current_height = self.controller.get_current_height()
            times = self.controller.get_height_times(height_times, current_height)
            if times >= 90:
                result = False
                break
            Logger.debug("{} current height: {}, times: {}".format(self.tag, current_height, times))

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

        self.controller.test_result(test_case, result)

    def rotation_onebyone_test(self):
        test_case = "2、ela node rotation one by one test"
        candidate_producers = self.controller.tx_manager.register_producers_list[
                              self.crc_number * 2: self.crc_number * 3]
        voted = False
        global current_vote_height
        global result
        global before_rotation_nicknames
        global after_rotation_nicknames

        before_rotation_nicknames = list()
        after_rotation_nicknames = list()
        current_vote_height = 0
        index = 0
        candidate = None

        height_times = dict()
        height_times[self.controller.get_current_height()] = 1

        time1 = datetime.now()
        while True:
            time2 = datetime.now()
            diff = (time2 - time1).seconds
            if diff >= 3 * 60:
                result = False
                break
            Logger.debug("{} diff: {} seconds".format(test_case, diff))
            current_height = self.controller.get_current_height()
            times = self.controller.get_height_times(height_times, current_height)
            Logger.debug("{} current height: {}, times: {}".format(self.tag, current_height, times))
            if times >= 90:
                result = False
                break

            self.controller.discrete_mining_blocks(1)
            if current_height > self.h2 + current_vote_height + 1:
                if not voted:
                    before_rotation_nicknames = self.controller.get_current_arbiter_nicknames()
                    before_rotation_nicknames.sort()
                    candidate = candidate_producers[index]
                    vote_amount = (len(candidate_producers) - index) * constant.TO_SELA * 100
                    ret = self.controller.tx_manager.vote_producer(self.tap_keystore, vote_amount, [candidate])
                    if ret:
                        Logger.info("vote {} ElAs at {} on success!".format((vote_amount / constant.TO_SELA),
                                                                            candidate.info.nickname))
                    else:
                        Logger.info("vote {} ElAs at {} failed!".format((vote_amount / constant.TO_SELA),
                                                                        candidate.info.nickname))
                        self.controller.terminate_all_process()
                    current_vote_height = current_height - self.h2
                    voted = True
            # if current_vote_height > 0:
            #     Logger.debug("last vote candidate height: {}".format(current_vote_height + self.h2))

            if current_height > self.h2 + current_vote_height + self.crc_number * 3 * 2:
                after_rotation_nicknames = self.controller.get_current_arbiter_nicknames()
                after_rotation_nicknames.sort()
                arbiters_list = rpc.get_arbiters_info()["arbiters"]
                ret = candidate.node.node_keystore.public_key.hex() in arbiters_list
                Logger.debug("{} before rotation nicknames: {}".format(self.tag, before_rotation_nicknames))
                Logger.debug("{} after  rotation nicknames: {}".format(self.tag, after_rotation_nicknames))
                self.controller.test_result("{} has rotated a producer!".format(candidate.info.nickname), ret)
                if ret:
                    voted = False
                    index += 1
            if index == 4:
                result = True
                break
            time.sleep(1)

        self.controller.test_result(test_case, result)

    def rotation_whole_test(self):
        test_case = "3、 ela node whole rotation test"
        global result
        register_producers = self.controller.tx_manager.register_producers_list
        vote_height = 0

        height_times = dict()
        height_times[self.controller.get_current_height()] = 1

        time1 = datetime.now()
        while True:
            time2 = datetime.now()
            diff = (time2 - time1).seconds
            Logger.debug("{} diff: {} seconds".format(test_case, diff))
            if diff >= 3 * 60:
                result = False
                break

            current_height = self.controller.get_current_height()
            times = self.controller.get_height_times(height_times, current_height)
            Logger.debug("{} current height: {}, times: {}".format(self.tag, current_height, times))
            if times >= 90:
                result = False
                break

            self.controller.discrete_mining_blocks(1)
            global before_rotation_nicknames

            if vote_height == 0 and current_height > self.h2:
                before_rotation_nicknames = self.controller.get_current_arbiter_nicknames()
                before_rotation_nicknames.sort()
                tap_balance = rpc.get_balance_by_address(self.tap_keystore.address)
                Logger.info("[test] tap_balance: {}".format(tap_balance))

                ret = self.controller.tx_manager.vote_producer(
                    keystore=self.tap_keystore,
                    amount=self.number * 10 * constant.TO_SELA,
                    candidates=register_producers[self.crc_number * 3: len(register_producers)-1],
                )
                if ret:
                    Logger.info("[test] candidate producers have voted on success again!!")
                else:
                    Logger.error("[test] candidate producers have voted failed!!")
                    break

                vote_height = current_height

            if vote_height > 0 and current_height > vote_height + self.crc_number * 3 * 2:
                after_rotation_nicknames = self.controller.get_current_arbiter_nicknames()
                after_rotation_nicknames.sort()
                arbiter_info = rpc.get_arbiters_info()
                arbiter = arbiter_info["arbiters"]
                arbiter_set = set(arbiter)

                candidate_publickey = list()
                for producer in register_producers[self.crc_number * 3: len(register_producers)-1]:
                    candidate_publickey.append(producer.node.node_keystore.public_key.hex())
                candidate_publickey_set = set(candidate_publickey)
                Logger.info("before rotation register producers: {}".format(before_rotation_nicknames))
                Logger.info("after  rotation register producers: {}".format(after_rotation_nicknames))
                if candidate_publickey_set.issubset(arbiter_set):
                    result = True
                    break
                else:
                    result = False
                    break

            time.sleep(1)

        self.controller.test_result(test_case, result)

    def minor_stop_test(self):
        test_case = "4、[stop minor ela nodes]"
        current_height = self.controller.get_current_height()
        if current_height < self.h2:
            return False

        inactive_nodes = self.controller.node_manager.ela_nodes[self.crc_number + 1: self.crc_number * 2]
        # candidate_nodes = self.controller.node_manager.ela_nodes_nodes[self.crc_number * 3 + 1: self.crc_number * 4]

        index = 0
        global stop_height
        global result
        inactive_nodes[index].stop()

        stop_height = self.controller.get_current_height() + self.crc_number * 3 * 1
        current_height = self.controller.get_current_height()
        time1 = datetime.now()

        height_times = dict()
        height_times[self.controller.get_current_height()] = 1

        test_case1 = "{} one node stops continue consensus".format(test_case)

        while current_height <= stop_height:
            time2 = datetime.now()
            diff = (time2 - time1).seconds
            Logger.debug("{} diff: {} seconds".format(self.tag, diff))
            if diff >= 2 * 60:
                result = False
                break

            self.controller.discrete_mining_blocks(1)
            current_height = self.controller.get_current_height()
            times = self.controller.get_height_times(height_times, current_height)
            Logger.debug("{} current height: {}, times: {}".format(self.tag, current_height, times))
            if times >= 90:
                result = False
                break

            time.sleep(1)

        if current_height >= stop_height:
            result = True

        self.controller.test_result(test_case1, result)

        index += 1
        test_case2 = "{} two nodes stop continue consensus".format(test_case)
        inactive_nodes[index].stop()
        stop_height = self.controller.get_current_height() + self.crc_number * 3 * 1
        time1 = datetime.now()
        while current_height <= stop_height:
            time2 = datetime.now()
            diff = (time2 - time1).seconds
            Logger.debug("{} diff: {} seconds".format(self.tag, diff))
            if diff >= 4 * 60:
                result = False
                break
            self.controller.discrete_mining_blocks(1)
            current_height = self.controller.get_current_height()
            times = self.controller.get_height_times(height_times, current_height)
            Logger.debug("{} current height: {}, times: {}".format(self.tag, current_height, times))
            if times >= 90:
                result = False
                break
            time.sleep(2)

        if current_height >= stop_height:
            result = True
        self.controller.test_result(test_case2, result)

        index += 1
        test_case3 = "{} three nodes stop continue consensus".format(test_case)
        inactive_nodes[index].stop()
        stop_height = self.controller.get_current_height() + self.crc_number * 3 * 1
        time1 = datetime.now()
        while current_height <= stop_height:
            time2 = datetime.now()
            diff = (time2 - time1).seconds
            Logger.debug("{} diff: {} seconds".format(self.tag, diff))
            if diff >= 6 * 60:
                result = False
                break
            self.controller.discrete_mining_blocks(1)
            current_height = self.controller.get_current_height()
            times = self.controller.get_height_times(height_times, current_height)
            Logger.debug("{} current height: {}, times: {}".format(self.tag, current_height, times))
            if times >= 90:
                result = False
                break
            time.sleep(6)

        if current_height >= stop_height:
            result = True
            for i in range(index + 1):
                inactive_nodes[i].start()
            time.sleep(1)
        self.controller.test_result(test_case3, result)

    def inactive_single_test(self):
        inactive_node_index = self.crc_number + 2
        global stop_height
        stop_height = 0
        test_case = "5、 Single Inactive and Arbiter Rotation"

        height_times = dict()
        height_times[self.controller.get_current_height()] = 1

        register_list = self.controller.tx_manager.register_producers_list
        inactive_producer = register_list[len(register_list) - 1]
        # replace_producer = self.controller.tx_manager.register_producers_list[]

        while True:
            current_height = self.controller.get_current_height()
            times = self.controller.get_height_times(height_times, current_height)
            Logger.info("{} current height: {}, times: {}".format(self.tag, current_height, times))

            if stop_height == 0 and current_height >= self.h2 + 1:
                self.controller.test_result("{} Ater H2".format(self.tag), True)
                self.controller.node_manager.ela_nodes[inactive_node_index].stop()
                stop_height = current_height
                Logger.error("{} node {} stopped at height {} on success!".format(self.tag,
                                                                                  inactive_node_index, stop_height))

            if stop_height != 0 and current_height >= stop_height + self.config["ela"]["max_inactivate_rounds"] + 12:
                deposit_address = self.controller.tx_manager.register_producers_list[1].deposit_address
                balance = rpc.get_balance_by_address(deposit_address)
                Logger.info("{} The balance of deposit address is {}".format(self.tag, balance))

                state = self.controller.get_producer_state(1)
                ret = state == "Inactivate"
                self.controller.test_result("{} Before active producer, the stopped producer state is Inactive".format(
                    self.tag), ret)
                ret = self.controller.tx_manager.activate_producer(inactive_producer)
                Logger.info("{} activate the producer result: {}".format(self.tag, ret))

                state = self.controller.get_producer_state(1)
                ret = state == "Activate"
                self.controller.test_result("{} After activate producer, the stopped producer state is active".format(
                    self.tag), ret)

                self.controller.test_result(test_case, ret)
                break

            time.sleep(1)
            self.controller.discrete_mining_blocks(1)

    def inactivate_much_test(self):
        pass

    def cross_normal_test(self):
        test_case = "6、[normal]"
        self.controller.show_current_height()
        ret = self.controller.tx_manager.cross_chain_transaction("did", True)
        self.controller.test_result("{} recharge to the side chain after H2".format(test_case), ret)
        time.sleep(2)
        ret = self.controller.tx_manager.cross_chain_transaction("did", False)
        self.controller.test_result("{} withdraw from the side chain after H2".format(test_case), ret)
        time.sleep(1)

    def cross_stop_test(self):
        test_case = "7、[exception]"
        self.controller.node_manager.arbiter_nodes[1].stop()
        self.controller.node_manager.did_nodes[1].stop()
        ret = self.controller.tx_manager.cross_chain_transaction("did", True)
        self.controller.test_result("{} stop one arbiter, test cross recharge".format(test_case), ret)

        self.controller.node_manager.did_nodes[1].stop()

    def after_test(self):
        self.controller.terminate_all_process()



