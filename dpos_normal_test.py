#!/usr/bin/env python
# -*- coding:utf-8 -*-
# date: 2019/4/8 9:45 AM
# author: liteng

import time

from src.tools.log import Logger
from src.control import Controller

config = {
    "ela": {
        "enable": True,
        "password": "123",
        "number": 12,
        "crc_number": 4,
        "later_start_number": 0,
        "pre_connect_offset": 5,
        "crc_dpos_height": 300,
        "public_dpos_height": 308
    },
    "side": False,
    "times": 1
}


def test_content():
    controller = Controller(config)
    controller.ready_for_dpos()
    h1 = controller.params.ela_params.crc_dpos_height
    h2 = controller.params.ela_params.public_dpos_height
    pre_offset = config["ela"]["pre_connect_offset"]
    number = controller.params.ela_params.number
    crc_number = controller.params.ela_params.crc_number
    later_start_number = controller.params.ela_params.later_start_number

    # init later start nodes include both registered and normal
    later_start_nodes = controller.node_manager.ela_nodes[number - later_start_number + 1: number + 1]

    current_height = controller.get_current_height()
    if current_height < h1 - pre_offset - 1:
        controller.discrete_mining_blocks(h1 - pre_offset - 1 - current_height)

    height_times = dict()
    height_times[current_height] = 1

    global result
    global start_height
    start_height = 0

    while True:
        current_height = controller.get_current_height()
        times = controller.get_height_times(height_times, current_height)
        Logger.debug("current height: {}, times: {}".format(current_height, times))

        if times >= 100:
            result = False
            break

        if current_height >= h1:
            controller.show_current_next_info()

        if current_height == h1 + 1:
            Logger.info("H1 PASS!")
            Logger.info("H1 PASS!")

        if current_height == h2 + 2:
            Logger.info("H2 PASS!")
            Logger.info("H2 PASS!")

        # current is equal 380, start the later nodes include two candidates and two normal nodes
        if later_start_number != 0 and start_height == 0 and current_height > h2 + crc_number * 3 * 6:
            for node in later_start_nodes:
                node.start()
            start_height = current_height

        if current_height > start_height + 500:
            result = True
            break

        controller.discrete_mining_blocks(1)
        time.sleep(1)

    controller.check_result("Dpos Normal Test", result)
    controller.terminate_all_process()


if __name__ == '__main__':

    for i in range(config["times"]):
        Logger.warn("[main] begin testing {} times".format(i+1))
        time.sleep(2)
        test_content()
        Logger.warn("[main] end testing {} times".format(i+1))
        time.sleep(3)


