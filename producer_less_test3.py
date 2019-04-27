#!/usr/bin/env python
# -*- coding:utf-8 -*-
# date: 2019/4/8 5:13 PM
# author: liteng

import time

from src.top.control import Controller

from src.middle.tools.log import Logger

config = {
    "ela": {
        "number": 12,
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
    controller.middle.ready_for_dpos()

    crc_number = controller.middle.params.ela_params.crc_number
    h1 = controller.middle.params.ela_params.crc_dpos_height
    h2 = controller.middle.params.ela_params.public_dpos_height
    pre_offset = config["ela"]["pre_connect_offset"]

    test_case = "More than 1/3 producers inactive and degenerate to CRC"
    inactive_producers_nodes = controller.middle.node_manager.ela_nodes[crc_number * 2 + 1:]

    inactive_public_keys = list()

    for node in inactive_producers_nodes:
        inactive_public_keys.append(node.node_keystore.public_key.hex())

    stop_height = 0

    current_height = controller.get_current_height()
    if current_height < h1 - pre_offset - 1:
        controller.discrete_mining_blocks(h1 - pre_offset - 1 - current_height)

    height_times = dict()
    height_times[current_height] = 1

    global result
    global restart
    restart = False

    while True:
        current_height = controller.get_current_height()
        times = controller.get_height_times(height_times, current_height)
        Logger.info("current height: {}, times: {}".format(current_height, times))
        if times >= 1000:
            result = False
            break

        if stop_height == 0 and current_height >= h2 + 12:
            for node in inactive_producers_nodes:
                node.stop()
            controller.test_result("Ater H2，stop 1/3 producers", True)

            stop_height = current_height
            Logger.debug("stop height: {}".format(stop_height))

        if stop_height != 0 and current_height >= stop_height:
            arbiters_nicknames = controller.get_current_arbiter_nicknames()
            arbiters_nicknames.sort()
            next_arbiter_nicknames = controller.get_next_arbiter_nicknames()
            next_arbiter_nicknames.sort()
            Logger.info("current arbiters nicknames: {}".format(arbiters_nicknames))
            Logger.info("next    arbiters nicknames: {}".format(next_arbiter_nicknames))

        if not restart and stop_height != 0 and current_height > stop_height + 24:
            crc_public_keys = controller.middle.keystore_manager.crc_public_keys
            current_arbiter_public_keys = controller.get_current_arbiter_public_keys()
            result = set(crc_public_keys) == set(current_arbiter_public_keys)

            Logger.debug("set crc public keys is equal set current arbiter public keys ?: {}".format(result))
            time.sleep(2)

            for node in inactive_producers_nodes:
                node.start()

            restart = True

        if stop_height != 0 and current_height > stop_height + 100:
            result = True
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



