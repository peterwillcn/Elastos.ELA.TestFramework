#!/usr/bin/env python
# -*- coding:utf-8 -*-
# date: 2019/4/8 5:13 PM
# author: liteng

import time

from src.control.control import Controller
from src.core.services import rpc
from src.tools.log import Logger

config = {
    "ela": {
        "number": 12,
        "crc_number": 4,
        "pre_connect_offset": 3,
        "crc_dpos_height": 300,
        "public_dpos_height": 308
    },
    "side": False,
    "times": 1
}


def test_content():
    controller = Controller(config)
    controller.ready_for_dpos()
    crc_number = controller.params.ela_params.crc_number
    h1 = controller.params.ela_params.crc_dpos_height
    h2 = controller.params.ela_params.public_dpos_height
    pre_offset = config["ela"]["pre_connect_offset"]
    test_case = "More than 1/3 crc inactive after 2 rotations restart crc can generate blocks"
    inactive_crc_nodes = controller.node_manager.ela_nodes[1: crc_number + 1]

    stop_height = 0
    global result
    global restart
    result = False
    restart = False

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
            controller.show_arbiter_info()

        if stop_height == 0 and current_height >= h2 + 12:
            controller.check_result("Ater H2，the first round of consensus", True)

            for node in inactive_crc_nodes:
                node.stop()

            stop_height = current_height
            print("stop_height : ", stop_height)

        if not restart and times >= 100:
            for node in inactive_crc_nodes:
                node.start()
                restart = True

        if stop_height != 0 and current_height > stop_height + 100:
            arbiters_list = rpc.get_arbiters_info()["arbiters"]
            result = set(controller.node_manager.normal_dpos_pubkeys) == set(arbiters_list)
            Logger.debug("normal arbiters dpos result: {}".format(result))
            controller.check_result("normal arbiters consensus", result)

        if stop_height != 0 and current_height > stop_height + 20:
            controller.start_later_nodes()
            result = controller.check_nodes_height()
            controller.check_result("check all the nodes height", result)
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



