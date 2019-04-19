#!/usr/bin/env python
# -*- coding:utf-8 -*-
# date: 2019/4/12 3:45 PM
# author: liteng

import time

from src.top.control import Controller

from src.middle.tools import constant
from src.middle.tools.log import Logger


config = {
    "ela": {
        "enable": True,
        "password": "123",
        "number": 20,
        "crc_number": 4,
        "pre_connect_offset": 3,
        "crc_dpos_height": 220,
        "public_dpos_height": 228
    },
    "side": False,
    "stop": True,
    "times": 1
}


def test_content():

    test_case = "Arbiter Whole Retation Test"
    control = Controller(config)
    control.middle.ready_for_dpos()

    h2 = control.middle.params.ela_params.public_dpos_height
    number = control.middle.params.ela_params.number
    crc_number = control.middle.params.ela_params.crc_number
    tap_keystore = control.get_tap_keystore()
    register_producers = control.middle.tx_manager.tx.register_producers_list

    vote_height = 0

    while True:
        current_height = control.get_current_height()
        Logger.debug("[test] current height: {}".format(current_height))
        control.discrete_mining_blocks(1)
        global before_rotation_nicknames

        if vote_height == 0 and current_height > h2 + 5:
            before_rotation_nicknames = control.get_current_arbiter_nicknames()
            before_rotation_nicknames.sort()
            tap_balance = control.middle.service_manager.rpc.get_balance_by_address(tap_keystore.address)
            Logger.info("[test] tap_balance: {}".format(tap_balance))

            ret = control.middle.tx_manager.tx.vote_producers(
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
            after_rotation_nicknames = control.get_current_arbiter_nicknames()
            after_rotation_nicknames.sort()
            arbiter_info = control.middle.service_manager.rpc.get_arbiters_info()
            arbiter = arbiter_info["arbiters"]
            arbiter_set = set(arbiter)
            candidate_public_key_set = set(control.middle.tx_manager.candidate_public_keys)
            general_public_key_set = set(control.middle.tx_manager.general_producer_public_keys)
            Logger.info("before rotation register producers: {}".format(before_rotation_nicknames))
            Logger.info("after  rotation register producers: {}".format(after_rotation_nicknames))
            if not general_public_key_set.issubset(arbiter_set) and candidate_public_key_set.issubset(arbiter_set):
                control.test_result(test_case, True)
                break
            else:
                control.test_result(test_case, False)

        time.sleep(1)

    time.sleep(2)
    control.terminate_all_process()


if __name__ == '__main__':

    times = config["times"]
    if times > 1:
        config["stop"] = True

    for i in range(config["times"]):
        Logger.warn("[main] begin testing {} times".format(i + 1))
        time.sleep(2)
        test_content()
        Logger.warn("[main] end testing {} times".format(i + 1))
        time.sleep(3)
