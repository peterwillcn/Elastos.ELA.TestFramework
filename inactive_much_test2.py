#!/usr/bin/env python
# -*- coding:utf-8 -*-
# date: 2019/4/8 5:13 PM
# author: liteng

import time

from src.top.control import Controller

from src.middle.tools.log import Logger

config = {
    "ela": {
        "number": 20,
        "crc_number": 4,
        "pre_connect_offset": 5,
        "crc_dpos_height": 200,
        "public_dpos_height": 208,
        "max_inactivate_rounds": 20
    },
    "side": False,
    "times": 1
}


def test_content():
    controller = Controller(config)
    controller.middle.ready_for_dpos()
    number = controller.middle.params.ela_params.number
    crc_number = controller.middle.params.ela_params.crc_number
    h1 = controller.middle.params.ela_params.crc_dpos_height
    h2 = controller.middle.params.ela_params.public_dpos_height
    pre_offset = config["ela"]["pre_connect_offset"]
    test_case = "More than 1/3 producers inactive first rotation still failed but second rotation on success "
    inactive_producers_nodes = controller.middle.node_manager.ela_nodes[crc_number * 2 + 1: crc_number * 4 + 1]
    replace_cadidates_nodes = controller.middle.node_manager.ela_nodes[crc_number * 4 + 1: number]

    inactive_public_keys = list()
    replace_public_keys = list()

    for node in inactive_producers_nodes:
        inactive_public_keys.append(node.node_keystore.public_key.hex())

    for node in replace_cadidates_nodes:
        replace_public_keys.append(node.node_keystore.public_key.hex())

    inactive_set = set(inactive_public_keys)
    replace_set = set(replace_public_keys)

    global result
    stop_height = 0

    height_times = dict()
    height_times[controller.get_current_height()] = 1

    while True:
        current_height = controller.get_current_height()
        times = controller.get_height_times(height_times, current_height)
        Logger.info("current height: {}, times: {}".format(current_height, times))
        if times >= 200:
            result = False
            break
        if current_height < h1 - pre_offset:
            controller.discrete_mining_blocks(h1 - pre_offset - current_height)
        controller.discrete_mining_blocks(1)
        if stop_height == 0 and current_height >= h2 + 12:
            controller.test_result("Ater H2，the first round of consensus", True)

            for node in inactive_producers_nodes:
                node.stop()

            stop_height = current_height
            print("stop_height 1: ", stop_height)
        if stop_height != 0 and current_height >= stop_height:
            arbiters_nicknames = controller.get_current_arbiter_nicknames()
            arbiters_nicknames.sort()
            next_arbiter_nicknames = controller.get_next_arbiter_nicknames()
            next_arbiter_nicknames.sort()
            Logger.info("current arbiters nicknames: {}".format(arbiters_nicknames))
            Logger.info("next    arbiters nicknames: {}".format(next_arbiter_nicknames))

        if stop_height != 0 and current_height > stop_height + 72:
            arbiters_set = set(controller.middle.service_manager.rpc.get_arbiters_info()["arbiters"])
            result = not inactive_set.issubset(arbiters_set) and replace_set.issubset(arbiters_set)
            break
        time.sleep(2)

    controller.test_result(test_case, result)

    controller.terminate_all_process()


if __name__ == '__main__':

    for i in range(config["times"]):
        Logger.warn("[main] begin testing {} times".format(i + 1))
        time.sleep(2)
        test_content()
        Logger.warn("[main] end testing {} times".format(i + 1))
        time.sleep(3)



