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
        "crc_dpos_height": 200,
        "public_dpos_height": 235
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
    "stop": True,
    "times": 1
}


def test_content():
    stop = config["stop"]
    controller = Controller(config)
    controller.middle.ready_for_dpos()
    time.sleep(3)
    controller.show_current_height()
    # Logger.info("######### [main] begin to test cross recharge and withdraw before H1 ########")
    # Logger.info("######### [main] begin to test cross recharge and withdraw before H1 ########")
    # ret = controller.middle.tx_manager.cross_chain_transaction(True)
    # controller.test_result("recharge to the side chain before H1", ret)
    # time.sleep(2)
    # ret = controller.middle.tx_manager.cross_chain_transaction(False)
    # controller.test_result("withdraw from the side chain before H1", ret)
    # time.sleep(1)
    # controller.show_current_height()
    #
    # current_height = controller.get_current_height()
    # Logger.debug("[main] current height: {}".format(current_height))
    #
    # Logger.info("######### [main] begin to test cross recharge and withdraw between H1 and H2 ########")
    # Logger.info("######### [main] begin to test cross recharge and withdraw between H1 and H2 ########")

    h1 = controller.middle.params.ela_params.crc_dpos_height
    current_height = controller.get_current_height()
    if current_height < h1 - 5:
        controller.discrete_mining_blocks(h1 - current_height - 5)

    while current_height <= h1 + 4:
        controller.discrete_mining_blocks(1)
        time.sleep(0.5)
        current_height = controller.get_current_height()
        Logger.debug("{} current height: {}".format("[main]", current_height))
    ret = controller.middle.tx_manager.cross_chain_transaction(True)
    controller.test_result("recharge to the side chain between H1 and H2", ret)
    time.sleep(2)
    ret = controller.middle.tx_manager.cross_chain_transaction(False)
    controller.test_result("withdraw from the side chain between H1 and H2", ret)
    time.sleep(1)

    h2 = controller.middle.params.ela_params.public_dpos_height

    Logger.info("######### [main] begin to test cross recharge and withdraw after H2 ########")
    Logger.info("######### [main] begin to test cross recharge and withdraw after H2 ########")

    while current_height <= h2 + 2:
        controller.discrete_mining_blocks(1)
        time.sleep(0.5)
        current_height = controller.get_current_height()
        Logger.debug("{} current height: {}".format("[main]", current_height))
    ret = controller.middle.tx_manager.cross_chain_transaction(True)
    controller.test_result("recharge to the side chain after H2", ret)
    time.sleep(2)
    ret = controller.middle.tx_manager.cross_chain_transaction(False)
    controller.test_result("withdraw from the side chain after H2", ret)
    time.sleep(1)

    if stop:
        controller.terminate_all_process()
    else:
        controller.loop_for_ever()


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