#!/usr/bin/env python
# -*- coding:utf-8 -*-
# date: 2019/4/8 9:45 AM
# author: liteng

import time

from src.tools.log import Logger
from src.control.control import Controller

from src.core.wallet.account import Account


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

    update_node_prikey = "aa8ad6d1ac6953f7b9a68b5b13fe79d7217fb687651c1c30be12e5e0328b667f"
    # update_producer_beforeh1 = controller.tx_manager.register_producers_list[0]
    update_producer = controller.tx_manager.register_producers_list[0]
    current_height = controller.get_current_height()
    if current_height < h1 - 5:
        controller.discrete_mining_blocks(h1 - 5 - current_height)

    height_times = dict()
    height_times[current_height] = 1

    global result
    global update_height
    update_height = 0

    while True:
        current_height = controller.get_current_height()
        times = controller.get_height_times(height_times, current_height)
        Logger.debug("current height: {}, times: {}".format(current_height, times))

        if times >= 100:
            result = False
            break
        if current_height >= h1:
            controller.show_arbiter_info()

        if update_height == 0 and current_height > h1 + 35:
            producer_payload = update_producer.producer_info()
            producer_payload.nickname = "^_^ HAHA"
            producer_payload.node_account = Account(update_node_prikey)

            producer_payload.url = "127.0.0.1"

            result = controller.tx_manager.update_producer(update_producer, producer_payload)
            controller.check_result(test_case, result)
            if result:
                controller.node_manager.node_pubkey_name_dict[update_node_prikey] = producer_payload.nickname
            update_height = current_height

        if current_height > h2 + 100:
            break

        controller.discrete_mining_blocks(1)
        time.sleep(1)

    controller.check_result(test_case, result)
    controller.terminate_all_process(result)


if __name__ == '__main__':

    for i in range(config["times"]):
        Logger.warn("[main] begin testing {} times".format(i+1))
        time.sleep(2)
        test_content()
        Logger.warn("[main] end testing {} times".format(i+1))
        time.sleep(3)




