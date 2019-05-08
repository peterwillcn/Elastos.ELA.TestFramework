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
        "pre_connect_offset": 30,
        "crc_dpos_height": 300,
        "public_dpos_height": 350
    },
    "side": False,
    "times": 1
}


def test_content():

    test_case = "update producer after pre offset but before h2"

    controller = Controller(config)
    controller.ready_for_dpos()
    h1 = controller.params.ela_params.crc_dpos_height
    h2 = controller.params.ela_params.public_dpos_height
    pre_offset = config["ela"]["pre_connect_offset"]

    will_update_producer = controller.tx_manager.register_producers_list[0]
    current_height = controller.get_current_height()
    if current_height < h1 - 5:
        controller.discrete_mining_blocks(h1 - pre_offset - 1 - current_height)

    height_times = dict()
    height_times[current_height] = 1

    global result
    global start_height
    update_height = 0

    while True:
        current_height = controller.get_current_height()
        times = controller.get_height_times(height_times, current_height)
        Logger.debug("current height: {}, times: {}".format(current_height, times))

        if times >= 100:
            result = False
            break

        if current_height >= h2:
            controller.show_current_next_info()

        if update_height == 0 and current_height > h1 + 35:
            producer_payload = will_update_producer.info

            # update nickname
            producer_payload.nickname = "^_^ HAHA"

            # update node public key
            producer_payload.node_public_key = \
                bytes.fromhex("0303710a960f04893281fe016ec7563a9c17fb8c7f0bea555b3a9349a6a1646479")

            result = controller.tx_manager.update_producer(will_update_producer, producer_payload)
            controller.test_result(test_case, result)
            update_height = current_height

        if current_height > h2 + 12:
            break

        controller.discrete_mining_blocks(1)
        time.sleep(1)

    controller.test_result(test_case, result)
    controller.terminate_all_process()


if __name__ == '__main__':

    for i in range(config["times"]):
        Logger.warn("[main] begin testing {} times".format(i+1))
        time.sleep(2)
        test_content()
        Logger.warn("[main] end testing {} times".format(i+1))
        time.sleep(3)


