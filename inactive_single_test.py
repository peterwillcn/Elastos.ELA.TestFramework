#!/usr/bin/env python
# -*- coding:utf-8 -*-
# date: 2019/4/8 5:13 PM
# author: liteng

import time

from src.top.control import Controller

from src.middle.tools.log import Logger

config = {
    "ela": {
        "number": 14,
        "crc_number": 4,
        "pre_connect_offset": 5,
        "crc_dpos_height": 180,
        "public_dpos_height": 188,
        "max_inactivate_rounds": 20
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

    inactive_node_index = crc_number + 2
    stop_height = 0
    test_case = "Single Inactive and Arbiter Rotation"
    inactive_producer = controller.middle.tx_manager.tx.register_producers_list[1]
    replace_producer = controller.middle.tx_manager.tx.register_producers_list[crc_number * 2]

    inactive_public_key = inactive_producer.node.node_keystore.public_key.hex()
    replace_public_key = replace_producer.node.node_keystore.public_key.hex()

    while True:
        current_height = controller.get_current_height()
        Logger.info("[main] current height: {}".format(current_height))
        # if current_height < h1 - 11:
        #     num = h1 - current_height - 11
        #     controller.discrete_mining_blocks(num)
        if stop_height == 0 and current_height >= h2 + 1:
            controller.test_result("Ater H2", True)
            controller.middle.node_manager.ela_nodes[inactive_node_index].stop()
            stop_height = current_height
            Logger.error("[main] node {} stopped at height {} on success!".format(inactive_node_index, stop_height))

        # if stop_height != 0 and current_height >= stop_height + config["ela"]["max_inactivate_rounds"] + 24:
        #     arbiters_info = controller.middle.service_manager.rpc.get_arbiters_info()
        #     arbiters_list = arbiters_info["arbiters"]
        #     print("arbiter_list {}".format(arbiters_list))
        #     Logger.debug("inactive public key: {}".format(inactive_public_key))
        #     Logger.debug("replace public key: {}".format(replace_public_key))
        #     ret = replace_public_key in arbiters_list and inactive_public_key not in arbiters_list
        #     controller.test_result(test_case, ret)

        if stop_height != 0 and current_height >= stop_height + config["ela"]["max_inactivate_rounds"] + 5:
            deposit_address = controller.middle.tx_manager.tx.register_producers_list[1].deposit_address
            balance = controller.middle.service_manager.rpc.get_balance_by_address(deposit_address)
            Logger.info("[main] The balance of deposit address is {}".format(balance))

            state = controller.get_producer_state(1)
            ret = state == "Inactivate"
            controller.test_result("Before active producer, the stopped producer state is Inactive", ret)
            ret = controller.middle.tx_manager.tx.activate_a_producer(inactive_producer)
            Logger.info("[main] activate the producer result: {}".format(ret))

            state = controller.get_producer_state(1)
            ret = state == "Activate"
            controller.test_result("After activate producer, the stopped producer state is active", ret)

            controller.test_result(test_case, ret)
            break

        time.sleep(1)
        controller.discrete_mining_blocks(1)

    controller.terminate_all_process()


if __name__ == '__main__':

    times = config["times"]

    for i in range(times):
        Logger.info("Start Testing {} times".format(i+1))
        time.sleep(1)
        test_content()
        time.sleep(1)
        Logger.info("End Testing {} times".format(i+1))
