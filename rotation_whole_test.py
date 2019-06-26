#!/usr/bin/env python
# -*- coding:utf-8 -*-
# date: 2019/4/12 3:45 PM
# author: liteng

import time

from src.control.control import Controller
from src.core.services import rpc
from src.tools import constant
from src.tools.log import Logger


config = {
    "ela": {
        "enable": True,
        "password": "123",
        "number": 24,
        "crc_number": 4,
        "later_start_number": 4,
        "pre_connect_offset": 5,
        "crc_dpos_height": 300,
        "public_dpos_height": 308
    },
    "side": False,
    "times": 1
}


def test_content():

    test_case = "Arbiter Whole Rotation Test"
    controller = Controller(config)
    controller.ready_for_dpos()

    h1 = controller.params.ela_params.crc_dpos_height
    h2 = controller.params.ela_params.public_dpos_height

    pre_offset = config["ela"]["pre_connect_offset"]
    number = controller.params.ela_params.number
    crc_number = controller.params.ela_params.crc_number

    global tap_account
    global result
    global check
    check = False
    result = False
    tap_account = controller.keystore_manager.tap_account
    register_producers = controller.tx_manager.register_producers_list

    vote_height = 0

    current_height = controller.get_current_height()
    if current_height < h1 - pre_offset - 1:
        controller.discrete_mining_blocks(h1 - pre_offset - 1 - current_height)

    height_times = dict()
    height_times[current_height] = 1

    while True:
        current_height = controller.get_current_height()
        times = controller.get_height_times(height_times, current_height)
        Logger.debug("current height: {}, times: {}".format(current_height, times))
        if times >= 100:
            controller.check_result(test_case, False)
            break

        global before_rotation_nicknames

        if current_height > h1:
            controller.show_arbiter_info()

        if vote_height == 0 and current_height > h2 + 12:
            before_rotation_nicknames = controller.get_arbiter_names("arbiters")
            before_rotation_nicknames.sort()
            tap_balance = rpc.get_balance_by_address(tap_account.address())
            Logger.info("tap_balance: {}".format(tap_balance))

            ret = controller.tx_manager.vote_producer(
                input_private_key=tap_account.private_key(),
                amount=number * constant.TO_SELA,
                candidates=register_producers[crc_number * 2: crc_number * 4]
            )
            controller.check_result("vote the candidates result", ret)
            vote_height = current_height

        if not check and vote_height > 0 and current_height > vote_height + crc_number * 3 * 2:
            after_rotation_nicknames = controller.get_arbiter_names("arbiters")
            after_rotation_nicknames.sort()
            arbiter_set = set(controller.get_current_arbiter_public_keys())
            Logger.info("before rotation register producers: {}".format(before_rotation_nicknames))
            Logger.info("after  rotation register producers: {}".format(after_rotation_nicknames))
            result = set(controller.get_node_public_keys(13, 21)).issubset(arbiter_set)
            controller.check_result(test_case, result)
            check = True

        if vote_height > 0 and current_height > vote_height + crc_number * 3 * 3:
            controller.start_later_nodes()
            result = controller.check_nodes_height()
            controller.check_result("check all the nodes have the same height", result)
            break

        controller.discrete_mining_blocks(1)
        time.sleep(1)

    time.sleep(2)
    controller.check_result(test_case, result)
    controller.terminate_all_process(result)


if __name__ == '__main__':

    for i in range(config["times"]):
        Logger.warn("[main] begin testing {} times".format(i + 1))
        time.sleep(2)
        test_content()
        Logger.warn("[main] end testing {} times".format(i + 1))
        time.sleep(3)
