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

    # test case title
    test_case = "Insufficient producers degradation cancel but not stop"
    # init for the controller that will deploy start nodes and recharge register vote producers before h1
    controller = Controller(config)
    controller.ready_for_dpos()

    # get some important params for later use
    h1 = controller.params.ela_params.crc_dpos_height
    h2 = controller.params.ela_params.public_dpos_height
    pre_offset = config["ela"]["pre_connect_offset"]

    # prepare  cancel producers, which number will be between 4 and 8
    cancel_height = 0
    cancel_count = random.randrange(4, 8)
    cancel_producers = controller.tx_manager.register_producers_list[: cancel_count]

    # mining the height to h1 - pre_connect_offset - 1
    current_height = controller.get_current_height()
    if current_height < h1 - pre_offset - 1:
        controller.discrete_mining_blocks(h1 - pre_offset - 1 - current_height)

    # height_times is for get the number of times of the same height
    height_times = dict()
    height_times[current_height] = 1

    global result
    global check
    result = False
    check = False

    while True:

        # get current height
        current_height = controller.get_current_height()

        # get number of times of the same height
        times = controller.get_height_times(height_times, current_height)
        Logger.info("current height: {}, times: {}".format(current_height, times))
        if times >= 1000:
            result = False
            break

        # after h1, show the current and next arbiters nicknames by sort
        if current_height >= h1:
            controller.show_current_next_info()

        # mining the height after h2 + 12, cancel producers which number is between 4 and 8 by random
        if cancel_height == 0 and current_height >= h2 + 12:
            Logger.info("will cancel {} producers:".format(cancel_count))
            time.sleep(2)
            for producer in cancel_producers:
                ret = controller.tx_manager.cancel_producer(producer)
                controller.check_result("Cancel Producer {}".format(producer.node.name), ret)

            cancel_height = current_height
            Logger.debug("cancel height: {}".format(cancel_height))

        # after the cancel_height + 36(356), will check the result and break to finish this test
        if not check and cancel_height != 0 and current_height > cancel_height + 36:
            crc_public_keys = controller.keystore_manager.crc_public_keys
            current_arbiter_public_keys = controller.get_current_arbiter_public_keys()
            result = set(crc_public_keys) == set(current_arbiter_public_keys)
            controller.check_result("Degradation to only CRC to consensus", result)
            controller.check_result("Degradation to only CRC to consensus", result)
            controller.start_later_nodes()
            check = True

        if cancel_height != 0 and current_height > cancel_height + 100:
            result = controller.check_nodes_height()
            controller.check_result("check all the nodes height", result)
            break

        controller.discrete_mining_blocks(1)
        time.sleep(1)

    # check result and terminate all the processes
    controller.check_result(test_case, result)
    controller.terminate_all_process()


if __name__ == '__main__':

    for i in range(config["times"]):
        Logger.warn("[main] begin testing {} times".format(i + 1))
        time.sleep(2)
        test_content()
        Logger.warn("[main] end testing {} times".format(i + 1))
        time.sleep(3)



