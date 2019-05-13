#!/usr/bin/env python
# -*- coding:utf-8 -*-
# date: 2019/4/8 5:13 PM
# author: liteng

import time
import random

from src.control import Controller

from src.tools.log import Logger

config = {
    "ela": {
        "number": 16,
        "crc_number": 4,
        "pre_connect_offset": 5,
        "crc_dpos_height": 300,
        "public_dpos_height": 308
    },
    "side": False,
    "times": 1
}


def test_content():

    controller = Controller(config)
    number = controller.params.ela_params.number
    crc_number = controller.params.ela_params.crc_number
    later_start_number = controller.params.ela_params.later_start_number
    h1 = controller.params.ela_params.crc_dpos_height
    h2 = controller.params.ela_params.public_dpos_height
    pre_offset = config["ela"]["pre_connect_offset"]
    test_case = "Pre connect before h2 and producers are not enough"

    will_register_count = random.randrange(2, 7)
    start = crc_number + 1
    end = crc_number + will_register_count + 1
    start2 = end
    end2 = number - later_start_number + 1
    Logger.debug("The number will be registered a producer are: {}".format(will_register_count))
    Logger.debug("start2 = {}, end2 = {}".format(start2, end2))
    controller.tx_manager.register_producers(start, end)
    controller.tx_manager.vote_producers(start, end)

    global result
    global re_register
    re_register = False

    crc_public_keys = controller.keystore_manager.crc_public_keys
    crc_public_keys.sort()

    arbiter_keystores = controller.keystore_manager.node_key_stores[1:13]
    target_public_keys = list()
    for keystore in arbiter_keystores:
        target_public_keys.append(keystore.public_key.hex())

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
            controller.show_current_next_info()

        if not re_register and current_height >= h2 + 12:

            current_arbiters = controller.get_current_arbiter_public_keys()
            current_arbiters.sort()
            Logger.debug("crc_public_keys:  {}".format(crc_public_keys))
            Logger.debug("current arbiters: {}".format(current_arbiters))
            result = set(current_arbiters) == set(crc_public_keys)
            Logger.debug("crc_public_keys is equal current arbiters: {}".format(result))
            controller.check_result("crc public key is equal current arbiter key", result)
            Logger.debug("will register producers number: {}".format(end2 - start2))
            time.sleep(3)

            ret = controller.tx_manager.register_producers(start2, end2, True)
            controller.check_result("register producers", ret)
            ret = controller.tx_manager.vote_producers(start2, end2)
            controller.check_result("vote producers", ret)
            controller.start_later_nodes()
            re_register = True

        if current_height >= h2 + 100:
            current_arbiter_keys = controller.get_current_arbiter_public_keys()
            controller.check_result("all nodes have the same height", controller.check_nodes_height())

            result = set(target_public_keys) == set(current_arbiter_keys)
            controller.check_result(test_case, result)
            break

        controller.discrete_mining_blocks(1)

        time.sleep(1)

    controller.terminate_all_process()


if __name__ == '__main__':

    for i in range(config["times"]):
        Logger.warn("[main] begin testing {} times".format(i + 1))
        time.sleep(2)
        test_content()
        Logger.warn("[main] end testing {} times".format(i + 1))
        time.sleep(3)



