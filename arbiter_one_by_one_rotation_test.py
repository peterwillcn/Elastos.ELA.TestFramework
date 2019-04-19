#!/usr/bin/env python
# -*- coding:utf-8 -*-
# date: 2019/4/13 1:40 PM
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
        "pre_connect_offset": 10,
        "crc_dpos_height": 220,
        "public_dpos_height": 240
    },
    "side": False,
    "stop": True,
    "times": 1
}


def one_by_one_rotation_test():
    test_case = "Arbiter One by One Rotation Test"
    control = Controller(config)
    control.middle.ready_for_dpos()

    h2 = control.middle.params.ela_params.public_dpos_height
    number = control.middle.params.ela_params.number
    crc_number = control.middle.params.ela_params.crc_number
    tap_keystore = control.get_tap_keystore()

    candidate_producers = control.middle.tx_manager.tx.register_producers_list[crc_number * 2: (number - crc_number)]
    voted = False
    global current_vote_height
    current_vote_height = 0
    index = 0
    candidate = None

    while True:
        current_height = control.get_current_height()
        Logger.debug("[test] current height: {}".format(current_height))
        control.discrete_mining_blocks(1)
        if current_height > h2 + current_vote_height + 1:
            if not voted:
                candidate = candidate_producers[index]
                vote_amount = (len(candidate_producers) - index) * constant.TO_SELA * 100
                ret = control.middle.tx_manager.tx.vote_a_producer(tap_keystore, candidate, vote_amount)
                if ret:
                    Logger.info("vote {} ElAs at {} on success!".format((vote_amount / constant.TO_SELA),
                                                                        candidate.payload.nickname))
                else:
                    Logger.info("vote {} ElAs at {} failed!".format((vote_amount / constant.TO_SELA),
                                                                    candidate.payload.nickname))
                    control.terminate_all_process()
                current_vote_height = current_height - h2
                voted = True
        if current_vote_height > 0:
            Logger.debug("last vote candidate height: {}".format(current_vote_height + h2))

        if current_height > h2 + current_vote_height + crc_number * 3 * 2:
            arbiters_list = control.middle.service_manager.rpc.get_arbiters_info()["arbiters"]
            ret = candidate.node.node_keystore.public_key.hex() in arbiters_list
            control.test_result("{} has rotated a producer!".format(candidate.payload.nickname), ret)
            if ret:
                voted = False
                index += 1
        if index == 8:
            break
        time.sleep(1)

    control.test_result(test_case, True)
    control.terminate_all_process()


if __name__ == '__main__':
    times = config["times"]
    if times > 1:
        config["stop"] = True

    for i in range(config["times"]):
        Logger.warn("[main] begin testing {} times".format(i + 1))
        time.sleep(2)
        one_by_one_rotation_test()
        Logger.warn("[main] end testing {} times".format(i + 1))
        time.sleep(3)