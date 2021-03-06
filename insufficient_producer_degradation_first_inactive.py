#!/usr/bin/env python
# -*- coding:utf-8 -*-
# date: 2019/4/8 5:13 PM
# author: liteng

import time

from src.control.control import Controller

from src.tools.log import Logger

config = {
    "ela": {
        "number": 16,
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
    test_case = "More than 1/3 producers inactive and degenerate to CRC"
    controller = Controller(config)
    controller.ready_for_dpos()

    crc_number = controller.params.ela_params.crc_number
    h1 = controller.params.ela_params.crc_dpos_height
    h2 = controller.params.ela_params.public_dpos_height
    pre_offset = config["ela"]["pre_connect_offset"]

    # get inactive producers [9,10,11,12]
    inactive_producers = controller.tx_manager.register_producers_list[crc_number: crc_number * 2]

    # get inactive nodes related to inactive producers
    inactive_producers_nodes = list()
    for producer in inactive_producers:
        inactive_producers_nodes.append(producer.node)

    # get inactive public keys related to inactive nodes
    inactive_public_keys = list()
    for node in inactive_producers_nodes:
        inactive_public_keys.append(node.get_node_public_key())

    stop_height = 0

    current_height = controller.get_current_height()
    if current_height < h1 - pre_offset - 1:
        controller.discrete_mining_blocks(h1 - pre_offset - 1 - current_height)

    height_times = dict()
    height_times[current_height] = 1

    global result
    global restart
    global activate
    result = False
    restart = False
    activate = False

    while True:
        current_height = controller.get_current_height()
        times = controller.get_height_times(height_times, current_height)
        Logger.info("current height: {}, times: {}".format(current_height, times))
        if times >= 1000:
            result = False
            break

        # after h1, show the current and next arbiters info by sort
        if current_height >= h1:
            controller.show_arbiter_info()

        if stop_height == 0 and current_height >= h2 + 12:
            for node in inactive_producers_nodes:
                node.stop()
            controller.check_result("Ater H2，stop 1/3 producers", True)

            stop_height = current_height
            Logger.debug("stop height: {}".format(stop_height))

        if not restart and stop_height != 0 and current_height > stop_height + 20:
            crc_public_keys = controller.keystore_manager.crc_public_keys
            current_arbiter_public_keys = controller.get_current_arbiter_public_keys()
            result = set(crc_public_keys) == set(current_arbiter_public_keys)

            Logger.debug("set crc public keys is equal set current arbiter public keys ?: {}".format(result))
            time.sleep(2)

            for node in inactive_producers_nodes:
                node.start()

            restart = True

        if not activate and stop_height != 0 and current_height > stop_height + 30:
            for producer in inactive_producers:
                ret = controller.tx_manager.active_producer(producer)
                controller.check_result("activate producer {}".format(producer.info.nickname), ret)
            controller.start_later_nodes()
            activate = True

        if stop_height != 0 and current_height > stop_height + 100:
            current_arbiter_public_keys = controller.get_current_arbiter_public_keys()
            controller.check_result("check all nodes have the same height", controller.check_nodes_height())

            result = set(inactive_public_keys).issubset(set(current_arbiter_public_keys))
            break

        controller.discrete_mining_blocks(1)
        time.sleep(1)

    controller.check_result(test_case, result)
    controller.terminate_all_process(result)


if __name__ == '__main__':

    for i in range(config["times"]):
        Logger.warn("[main] begin testing {} times".format(i + 1))
        time.sleep(2)
        test_content()
        Logger.warn("[main] end testing {} times".format(i + 1))
        time.sleep(3)



