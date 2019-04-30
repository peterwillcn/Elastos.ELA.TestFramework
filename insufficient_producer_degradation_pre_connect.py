#!/usr/bin/env python
# -*- coding:utf-8 -*-
# date: 2019/4/8 5:13 PM
# author: liteng

import time
import random

from src.top.control import Controller

from src.middle.tools.log import Logger

config = {
    "ela": {
        "number": 16,
        "crc_number": 4,
        "pre_connect_offset": 5,
        "crc_dpos_height": 300,
        "public_dpos_height": 320,
        "max_inactivate_rounds": 20
    },
    "side": False,
    "times": 1
}


def test_content():
    controller = Controller(config)
    number = controller.middle.params.ela_params.number
    crc_number = controller.middle.params.ela_params.crc_number
    h1 = controller.middle.params.ela_params.crc_dpos_height
    h2 = controller.middle.params.ela_params.public_dpos_height
    pre_offset = config["ela"]["pre_connect_offset"]
    test_case = "Pre connect before h2 and producers are not enough"

    will_register_count = random.randrange(2, 7)
    start = crc_number + 1
    end = crc_number + will_register_count + 1
    start2 = end
    end2 = number
    Logger.debug("The number will be registered a producer are: {}".format(will_register_count))
    controller.middle.tx_manager.register_producers(start, end)
    controller.middle.tx_manager.vote_producers(start, end)

    global result
    global re_register
    re_register = False
    crc_public_keys = controller.middle.keystore_manager.crc_public_keys
    crc_public_keys.sort()

    current_height = controller.get_current_height()
    if current_height < h1 - pre_offset - 1:
        controller.discrete_mining_blocks(h1 - pre_offset - 1 - current_height)

    height_times = dict()
    height_times[current_height] = 1

    while True:
        current_height = controller.get_current_height()
        times = controller.get_height_times(height_times, current_height)
        Logger.info("current height: {}, times: {}".format(current_height, times))
        if times >= 1000:
            result = False
            break

        if current_height > h1:
            current_nick_names = controller.get_current_arbiter_nicknames()
            current_nick_names.sort()
            next_nick_names = controller.get_next_arbiter_nicknames()
            next_nick_names.sort()
            Logger.debug("current arbiters: {}".format(current_nick_names))
            Logger.debug("next    arbiters: {}".format(next_nick_names))

        if not re_register and current_height >= h2 + 12:

            current_arbiters = controller.get_current_arbiter_public_keys()
            current_arbiters.sort()
            Logger.debug("crc_public_keys:  {}".format(crc_public_keys))
            Logger.debug("current arbiters: {}".format(current_arbiters))
            result = set(current_arbiters) == set(crc_public_keys)
            Logger.debug("crc_public_keys is equal current arbiters: {}".format(result))

            controller.middle.tx_manager.register_producers(start2, end2, True)
            controller.middle.tx_manager.vote_producers(start2, end2)
            re_register = True

        if current_height >= h2 + 200:
            break

        controller.discrete_mining_blocks(1)

        time.sleep(1)

    controller.test_result(test_case, result)
    controller.terminate_all_process()


if __name__ == '__main__':

    for i in range(config["times"]):
        Logger.warn("[main] begin testing {} times".format(i + 1))
        time.sleep(2)
        test_content()
        Logger.warn("[main] end testing {} times".format(i + 1))
        time.sleep(3)



