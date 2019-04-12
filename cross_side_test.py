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
        "crc_dpos_height": 220,
        "public_dpos_height": 200000
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
    "times": 3
}


def test_content():
    stop = config["stop"]
    controller = Controller(config)
    controller.middle.ready_for_dpos()
    time.sleep(3)
    current_height = controller.get_current_height()
    Logger.debug("[main] current height: {}".format(current_height))
    Logger.info("######### [main] begin to test cross recharge and withdraw before H1 ########")
    Logger.info("######### [main] begin to test cross recharge and withdraw before H1 ########")
    controller.middle.tx_manager.cross_chain_transaction(True)
    time.sleep(2)
    controller.middle.tx_manager.cross_chain_transaction(False)
    time.sleep(1)

    current_height = controller.get_current_height()
    Logger.debug("[main] current height: {}".format(current_height))

    Logger.info("######### [main] begin to test cross recharge and withdraw between H1 and H2 ########")
    Logger.info("######### [main] begin to test cross recharge and withdraw between H1 and H2 ########")

    h2 = controller.middle.params.ela_params.crc_dpos_height
    Logger.info("[main] h1: {}".format(h2))
    Logger.info("[main] h1: {}".format(h2))
    Logger.info("[main] h1: {}".format(h2))
    while current_height <= controller.middle.params.ela_params.crc_dpos_height + 10:
        controller.discrete_mining_blocks(1)
        time.sleep(0.5)
        current_height = controller.get_current_height()
        Logger.debug("{} current height: {}".format("[main]", current_height))
    controller.middle.tx_manager.cross_chain_transaction(True)
    time.sleep(2)
    controller.middle.tx_manager.cross_chain_transaction(False)
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