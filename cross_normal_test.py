#!/usr/bin/env python
# -*- coding:utf-8 -*-
# date: 2019/4/8 11:32 AM
# author: liteng

import time

from src.middle.tools.log import Logger

from src.top.control import Controller

config = {
    "ela": {
        "number": 12,
        "crc_number": 4,
        "pre_connect_offset": 5,
        "crc_dpos_height": 300,
        "public_dpos_height": 335
    },
    "side": True,
    "arbiter": {
        "enable": True,
        "number": 9,
        "pow_chain": True,
        "print_level": 0
    },
    "did": {
        "enable": True,
        "number": 5,
        "instant_block": True
    },
    "token": {
        "enable": True,
        "number": 5,
        "instant_block": True
    },
    "times": 1
}


def test_content():
    controller = Controller(config)
    controller.middle.ready_for_dpos()

    h1 = controller.middle.params.ela_params.crc_dpos_height
    h2 = controller.middle.params.ela_params.public_dpos_height
    pre_offset = config["ela"]["pre_connect_offset"]

    global test_case
    # test_case = "cross recharge before H1"
    current_height = controller.get_current_height()
    # Logger.debug("current height: {}".format(current_height))
    # Logger.info("### Testing {} ###".format(test_case))
    # time.sleep(2)
    # ret = controller.middle.tx_manager.cross_chain_transaction("did", True)
    # controller.test_result(test_case, ret)
    #
    # test_case = "cross withdraw before H1"
    # current_height = controller.get_current_height()
    # Logger.debug("current height: {}".format(current_height))
    # Logger.info("### Testing {} ###".format(test_case))
    # time.sleep(2)
    # ret = controller.middle.tx_manager.cross_chain_transaction("did", False)
    # controller.test_result(test_case, ret)
    #
    # current_height = controller.get_current_height()
    # Logger.debug("current height: {}".format(current_height))

    if current_height < h1 - pre_offset - 1:
        controller.discrete_mining_blocks(h1 - pre_offset - 1 - current_height)

    height_times = dict()
    height_times[current_height] = 1

    global result

    while True:
        current_height = controller.get_current_height()
        times = controller.get_height_times(height_times, current_height)
        Logger.debug("current height: {}, times: {}".format(current_height, times))

        if times >= 100:
            result = False
            break

        if current_height > h1 + 4:
            test_case = "cross chain recharge between H1 and H2"
            Logger.info("### Testing {} ###".format(test_case))
            result = controller.middle.tx_manager.cross_chain_transaction("did", True)
            controller.test_result(test_case, result)

            controller.discrete_mining_blocks(1)
            test_case = "cross chain withdraw between H1 and H2"
            Logger.info("### Testing {} ###".format(test_case))
            result = controller.middle.tx_manager.cross_chain_transaction("did", False)
            controller.test_result(test_case, result)

        if current_height > h2 + 12:
            test_case = "cross chain recharge after H2"
            Logger.info("### Testing {} ###".format(test_case))
            result = controller.middle.tx_manager.cross_chain_transaction("token", True)
            controller.test_result(test_case, result)

            controller.discrete_mining_blocks(1)
            test_case = "cross chain withdraw between after H2"
            Logger.info("### Testing {} ###".format(test_case))
            result = controller.middle.tx_manager.cross_chain_transaction("token", False)
            controller.test_result(test_case, result)

            if result:
                break

        controller.discrete_mining_blocks(1)
        time.sleep(1)

    controller.terminate_all_process()


if __name__ == '__main__':

    times = config["times"]
    if times > 1:
        config["stop"] = True

    for i in range(config["times"]):
        Logger.warn("[main] begin testing {} times".format(i+1))
        time.sleep(2)
        test_content()
        Logger.warn("[main] end testing {} times".format(i+1))
        time.sleep(3)