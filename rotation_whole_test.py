#!/usr/bin/env python
# -*- coding:utf-8 -*-
# date: 2019/4/12 3:45 PM
# author: liteng

import time

from src.control import Controller
from src.core.services import rpc
from src.tools import constant
from src.tools.log import Logger


config = {
    "ela": {
        "enable": True,
        "password": "123",
        "number": 20,
        "crc_number": 4,
        "pre_connect_offset": 5,
        "crc_dpos_height": 300,
        "public_dpos_height": 308
    },
    "side": False,
    "times": 1
}


def test_content():

    test_case = "Arbiter Whole Retation Test"
    controller = Controller(config)
    controller.ready_for_dpos()

    h1 = controller.params.ela_params.crc_dpos_height
    h2 = controller.params.ela_params.public_dpos_height

    pre_offset = config["ela"]["pre_connect_offset"]
    number = controller.params.ela_params.number
    crc_number = controller.params.ela_params.crc_number
    tap_keystore = controller.keystore_manager.tap_key_store
    register_producers = controller.tx_manager.tx.register_producers_list

    vote_height = 0

    current_height = controller.get_current_height()
    if current_height < h1 - pre_offset - 1:
        controller.discrete_mining_blocks(h1 - pre_offset - 1 - current_height)

    height_times = dict()
    height_times[current_height] = 1

    while True:
        current_height = controller.get_current_height()
        times = controller.get_height_times(height_times, current_height)
        Logger.debug("[test] current height: {}, times: {}".format(current_height, times))
        if times >= 100:
            controller.test_result(test_case, False)
            break

        controller.discrete_mining_blocks(1)
        global before_rotation_nicknames

        if vote_height == 0 and current_height > h2 + 5:
            before_rotation_nicknames = controller.get_current_arbiter_nicknames()
            before_rotation_nicknames.sort()
            tap_balance = rpc.get_balance_by_address(tap_keystore.address)
            Logger.info("[test] tap_balance: {}".format(tap_balance))

            ret = controller.tx_manager.tx.vote_producers(
                vote_keystore=tap_keystore,
                producers=register_producers[crc_number * 2: len(register_producers)],
                vote_amount=number * constant.TO_SELA
            )
            if ret:
                Logger.info("[test] candidate producers have voted on success again!!")
            else:
                Logger.error("[test] candidate producers have voted failed!!")
                break

            vote_height = current_height

        if vote_height > 0 and current_height > vote_height + crc_number * 3 * 2:
            after_rotation_nicknames = controller.get_current_arbiter_nicknames()
            after_rotation_nicknames.sort()
            arbiter_info = rpc.get_arbiters_info()
            arbiter = arbiter_info["arbiters"]
            arbiter_set = set(arbiter)
            candidate_public_key_set = set(controller.tx_manager.candidate_public_keys)
            general_public_key_set = set(controller.tx_manager.general_producer_public_keys)
            Logger.info("before rotation register producers: {}".format(before_rotation_nicknames))
            Logger.info("after  rotation register producers: {}".format(after_rotation_nicknames))
            if not general_public_key_set.issubset(arbiter_set) and candidate_public_key_set.issubset(arbiter_set):
                controller.test_result(test_case, True)
                break
            else:
                controller.test_result(test_case, False)

        time.sleep(1)

    time.sleep(2)
    controller.terminate_all_process()


if __name__ == '__main__':

    for i in range(config["times"]):
        Logger.warn("[main] begin testing {} times".format(i + 1))
        time.sleep(2)
        test_content()
        Logger.warn("[main] end testing {} times".format(i + 1))
        time.sleep(3)
