#!/usr/bin/env python
# -*- coding:utf-8 -*-
# date: 2019/4/8 5:13 PM
# author: liteng

import time

from src.control import Controller

from src.tools.log import Logger

config = {
    "ela": {
        "number": 20,
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
    controller.ready_for_dpos()

    number = controller.params.ela_params.number
    crc_number = controller.params.ela_params.crc_number
    h1 = controller.params.ela_params.crc_dpos_height
    h2 = controller.params.ela_params.public_dpos_height
    pre_offset = config["ela"]["pre_connect_offset"]

    test_case = "More than 1/3 producers inactive both first and second rotation failed and finally degenerate to CRC"
    inactive_producers = controller.tx_manager.register_producers_list[4:]

    target_arbiters = controller.keystore_manager.node_key_stores[1: 13]
    target_public_keys = list()
    for keystore in target_arbiters:
        target_public_keys.append(keystore.public_key.hex())

    stop_height = 0

    global result
    global activate
    global current_arbiter_public_keys
    activate = False

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
            controller.show_current_next_info()

        if stop_height == 0 and current_height >= h2 + 12:
            controller.test_result("Ater H2，the first round of consensus", True)

            for producer in inactive_producers:
                producer.node.stop()

            stop_height = current_height
            print("stop_height 1: ", stop_height)

        if not activate and stop_height != 0 and current_height > stop_height + 20:
            inactive_producers = inactive_producers[:4]
            for producer in inactive_producers:
                producer.node.start()

            for producer in inactive_producers:
                ret = controller.tx_manager.activate_producer(producer)
                controller.test_result("activate producer {}".format(producer.info.nickname), ret)
            activate = True

        if stop_height != 0 and current_height > stop_height + 200:
            current_arbiter_public_keys = controller.get_current_arbiter_public_keys()
            result = set(target_public_keys).issubset(current_arbiter_public_keys)
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



