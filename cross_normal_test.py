#!/usr/bin/env python
# -*- coding:utf-8 -*-
# date: 2019/4/8 11:32 AM
# author: liteng

import time

from src.tools.log import Logger

from src.control import Controller

config = {
    "ela": {
        "number": 12,
        "crc_number": 4,
        "pre_connect_offset": 5,
        "crc_dpos_height": 400,
        "public_dpos_height": 500
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
        "enable": False,
        "number": 5,
        "instant_block": True
    },
    "times": 1
}


def test_content():
    controller = Controller(config)
    controller.ready_for_dpos()

    h1 = controller.params.ela_params.crc_dpos_height
    h2 = controller.params.ela_params.public_dpos_height
    pre_offset = config["ela"]["pre_connect_offset"]
    token_enable = config["token"]["enable"]

    global test_case
    before_h1 = False
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

        if not before_h1 and current_height > h1 + 4:
            before_h1 = True
            test_case = "cross chain recharge did between H1 and H2"
            Logger.info("### Testing {} ###".format(test_case))
            result = controller.tx_manager.cross_chain_transaction("did", True)
            controller.test_result(test_case, result)

            if token_enable:
                test_case = "cross chain recharge token between H1 and H2"
                Logger.info("### Testing {} ###".format(test_case))
                result = controller.tx_manager.cross_chain_transaction("token", True)
                controller.test_result(test_case, result)

            controller.discrete_mining_blocks(1)
            time.sleep(2)
            controller.discrete_mining_blocks(1)
            time.sleep(2)
            controller.discrete_mining_blocks(1)
            test_case = "cross chain withdraw did between H1 and H2"
            Logger.info("### Testing {} ###".format(test_case))
            result = controller.tx_manager.cross_chain_transaction("did", False)
            controller.test_result(test_case, result)

            if token_enable:
                controller.discrete_mining_blocks(1)
                test_case = "cross chain withdraw token between H1 and H2"
                Logger.info("### Testing {} ###".format(test_case))
                result = controller.tx_manager.cross_chain_transaction("token", False)
                controller.test_result(test_case, result)

        if current_height > h2 + 1:
            test_case = "cross chain recharge did after H2"
            Logger.info("### Testing {} ###".format(test_case))
            result = controller.tx_manager.cross_chain_transaction("did", True)
            controller.test_result(test_case, result)

            if token_enable:
                test_case = "cross chain recharge token after H2"
                Logger.info("### Testing {} ###".format(test_case))
                result = controller.tx_manager.cross_chain_transaction("token", True)
                controller.test_result(test_case, result)

            controller.discrete_mining_blocks(1)
            test_case = "cross chain withdraw did after H2"
            Logger.info("### Testing {} ###".format(test_case))
            result = controller.tx_manager.cross_chain_transaction("did", False)
            controller.test_result(test_case, result)

            if token_enable:
                controller.discrete_mining_blocks(1)
                test_case = "cross chain withdraw token after H2"
                Logger.info("### Testing {} ###".format(test_case))
                result = controller.tx_manager.cross_chain_transaction("token", False)
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