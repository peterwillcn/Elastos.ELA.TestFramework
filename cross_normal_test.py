#!/usr/bin/env python
# -*- coding:utf-8 -*-
# date: 2019/4/8 11:32 AM
# author: liteng


import time

from src.tools.log import Logger

from src.control.control import Controller

config = {
    "ela": {
        "number": 6,
        "crc_number": 2,
        "later_start_number": 0,
        "pre_connect_offset": 5,
        "crc_dpos_height": 300,
        "public_dpos_height": 308,
        "cr_committee_start_height": 350
    },
    "side": True,
    "arbiter": {
        "enable": True,
        "number": 2,
        "pow_chain": True,
        "print_level": 0
    },
    "did": {
        "enable": True,
        "number": 2,
        "instant_block": True
    },
    "token": {
        "enable": False,
        "number": 2,
        "instant_block": True
    },
    "neo": {
        "enable": False,
        "number": 2,
        "instant_block": True
    },
    "geth": {
        "enable": False,
        "number": 2,
        "instant_block": True
    },
    "times": 1
}


def test_content():
    controller = Controller(config)
    controller.ready_for_dpos()

    h1 = controller.params.ela_params.crc_dpos_height
    h2 = controller.params.ela_params.public_dpos_height
    h3 = controller.params.ela_params.cr_committee_start_height
    pre_offset = config["ela"]["pre_connect_offset"]
    did_enable = config["did"]["enable"]
    token_enable = config["token"]["enable"]
    neo_enable = config["neo"]["enable"]

    global test_case
    current_height = controller.get_current_height()

    if current_height < h1 - pre_offset - 1:
        controller.discrete_mining_blocks(h1 - pre_offset - 1 - current_height)

    height_times = dict()
    height_times[current_height] = 1

    global result
    global before_h1
    before_h1 = True

    while True:
        current_height = controller.get_current_height()
        times = controller.get_height_times(height_times, current_height)
        Logger.debug("current height: {}, times: {}".format(current_height, times))

        if times >= 100:
            result = False
            break

        # if before_h1 and current_height > h1 + 1:
        #     before_h1 = False
        #
        #     if did_enable:
        #         test_case = "cross chain recharge did between H1 and H2"
        #         Logger.info("### Testing {} ###".format(test_case))
        #         result = controller.tx_manager.cross_chain_transaction("did", True)
        #         controller.check_result(test_case, result)
        #
        #         controller.discrete_mining_blocks(1)
        #         time.sleep(2)
        #         controller.discrete_mining_blocks(1)
        #
        #         test_case = "cross chain withdraw did between H1 and H2"
        #         Logger.info("### Testing {} ###".format(test_case))
        #         result = controller.tx_manager.cross_chain_transaction("did", False)
        #         controller.check_result(test_case, result)
        #
        #         controller.discrete_mining_blocks(1)
        #         time.sleep(2)
        #         controller.discrete_mining_blocks(1)
        #         time.sleep(2)
        #
        #     if neo_enable:
        #         test_case = "cross chain recharge neo between H1 and H2"
        #         Logger.info("### Testing {} ###".format(test_case))
        #         result = controller.tx_manager.cross_chain_transaction("neo", True)
        #         controller.check_result(test_case, result)
        #
        #         controller.discrete_mining_blocks(1)
        #         time.sleep(2)
        #         controller.discrete_mining_blocks(1)
        #         time.sleep(2)
        #
        #         test_case = "cross chain withdraw neo between H1 and H2"
        #         Logger.info("### Testing {} ###".format(test_case))
        #         result = controller.tx_manager.cross_chain_transaction("neo", False)
        #         controller.check_result(test_case, result)

        if current_height == h2 + 2:
            Logger.info("H2 PASS!")
            Logger.info("H2 PASS!")

            # register cr
            controller.ready_for_cr()

        if current_height == h3 + 1:
            if did_enable:
                test_case = "cross chain recharge did after H3"
                Logger.info("### Testing {} ###".format(test_case))
                result = controller.tx_manager.cross_chain_transaction("did", True)
                controller.check_result(test_case, result)

                controller.discrete_mining_blocks(1)
                time.sleep(2)
                controller.discrete_mining_blocks(1)
                time.sleep(2)

                test_case = "cross chain withdraw did after H3"
                Logger.info("### Testing {} ###".format(test_case))
                result = controller.tx_manager.cross_chain_transaction("did", False)
                controller.check_result(test_case, result)

                controller.discrete_mining_blocks(1)
                time.sleep(2)
                controller.discrete_mining_blocks(1)
                time.sleep(2)

            if token_enable:
                test_case = "cross chain recharge token after H3"
                Logger.info("### Testing {} ###".format(test_case))
                result = controller.tx_manager.cross_chain_transaction("token", True)
                controller.check_result(test_case, result)

                controller.discrete_mining_blocks(1)
                time.sleep(2)
                controller.discrete_mining_blocks(1)
                time.sleep(2)

                test_case = "cross chain withdraw token after H3"
                Logger.info("### Testing {} ###".format(test_case))
                result = controller.tx_manager.cross_chain_transaction("token", False)
                controller.check_result(test_case, result)

                controller.discrete_mining_blocks(1)
                time.sleep(2)
                controller.discrete_mining_blocks(1)
                time.sleep(2)

            if neo_enable:
                test_case = "cross chain recharge noe after H3"
                Logger.info("### Testing {} ###".format(test_case))
                result = controller.tx_manager.cross_chain_transaction("neo", True)
                controller.check_result(test_case, result)

                controller.discrete_mining_blocks(1)
                time.sleep(2)
                controller.discrete_mining_blocks(1)
                time.sleep(2)

                test_case = "cross chain withdraw neo after H3"
                Logger.info("### Testing {} ###".format(test_case))
                result = controller.tx_manager.cross_chain_transaction("neo", False)
                controller.check_result(test_case, result)

            Logger.debug("Start later nodes and check all nodes height")
            controller.start_later_nodes()
            result = controller.check_nodes_height()
            controller.check_result("check all nodes height", result)
            break

        controller.discrete_mining_blocks(1)
        time.sleep(1)

    controller.check_result(test_case, result)
    controller.terminate_all_process(result)


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

