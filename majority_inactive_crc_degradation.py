#!/usr/bin/env python
# -*- coding:utf-8 -*-
# date: 2019/4/8 5:13 PM
# author: liteng

import time

from src.control.control import Controller

from src.tools.log import Logger

config = {
    "ela": {
        "number": 24,
        "crc_number": 4,
        "pre_connect_offset": 5,
        "later_start_number": 4,
        "crc_dpos_height": 300,
        "public_dpos_height": 308
    },
    "side": False,
    "times": 1
}


def test_content():
    controller = Controller(config)
    controller.ready_for_dpos()

    number = controller.params.ela_params.number
    crc_number = controller.params.ela_params.crc_number
    later_start_number = controller.params.ela_params.later_start_number
    h1 = controller.params.ela_params.crc_dpos_height
    h2 = controller.params.ela_params.public_dpos_height
    pre_offset = config["ela"]["pre_connect_offset"]

    test_case = "Majority inactive degradation to CRC"

    # init inactive producers [5,6,7,8, 9,10,11,12, 13,14,15,16]
    inactive_producers = controller.tx_manager.register_producers_list[4: 16]
    inactive_nodes = list()

    for producer in inactive_producers:
        inactive_nodes.append(producer.node)

    stop_height = 0

    global result
    global activate
    global current_arbiter_public_keys
    result = False
    activate = False
    current_arbiter_public_keys = list()

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

        # after h1, show the current and next arbiters info
        if current_height >= h1:
            controller.show_arbiter_info()

        if stop_height == 0 and current_height >= h2 + 12:
            controller.check_result("Ater H2，the first round of consensus", True)

            for node in inactive_nodes:
                node.stop()

            stop_height = current_height
            print("stop_height 1: ", stop_height)

        if not activate and stop_height != 0 and current_height > stop_height + 20:
            first_inactive_producers = inactive_producers[:4]
            first_inactive_nodes = inactive_nodes[:4]
            for node in first_inactive_nodes:
                node.start()

            for producer in first_inactive_producers:
                ret = controller.tx_manager.active_producer(producer)
                controller.check_result("activate producer {}".format(producer.info.nickname), ret)

            # start stopped nodes again and look at their height are sync them
            controller.start_stop_nodes()
            activate = True

        if stop_height != 0 and current_height > stop_height + 100:
            current_arbiter_public_keys = controller.get_current_arbiter_public_keys()
            controller.check_result("check all nodes have the same height", controller.check_nodes_height())
            result = set(controller.node_manager.normal_dpos_pubkeys).issubset(current_arbiter_public_keys)
            break

        controller.discrete_mining_blocks(1)
        time.sleep(1)

    controller.check_result(test_case, result)
    controller.terminate_all_process()


if __name__ == '__main__':

    for i in range(config["times"]):
        Logger.warn("[main] begin testing {} times".format(i + 1))
        time.sleep(2)
        test_content()
        Logger.warn("[main] end testing {} times".format(i + 1))
        time.sleep(3)



