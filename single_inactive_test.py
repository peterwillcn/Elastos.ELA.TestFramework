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
        "pre_connect_offset": 20,
        "crc_dpos_height": 200,
        "public_dpos_height": 230,
        "max_inactivate_rounds": 20
    },
    "side": False
}


if __name__ == '__main__':

    controller = Controller(config)
    controller.middle.ready_for_dpos()
    index = controller.middle.params.ela_params.crc_number + 1
    stop_height = 0
    first_time = False
    test_case = "Single Inactive and Arbiter Rotation"
    inactive_producer = controller.middle.tx_manager.tx.register_producers_list[1]
    replace_producer = controller.middle.tx_manager.tx.register_producers_list[
        controller.middle.params.ela_params.crc_number * 2
    ]

    inactive_public_key = inactive_producer.node.node_keystore.public_key.hex()
    replace_public_key = replace_producer.node.node_keystore.public_key.hex()

    while True:
        current_height = controller.get_current_height()
        Logger.info("[main] current height: {}".format(current_height))
        if current_height == controller.middle.params.ela_params.public_dpos_height + 1:
            controller.test_result("Ater H2", True)
        if not first_time and current_height >= controller.middle.params.ela_params.public_dpos_height \
                + controller.middle.params.ela_params.crc_number * 3:
            controller.middle.node_manager.ela_nodes[index].stop()
            stop_height = current_height
            first_time = True
            Logger.error("[main] node {} stopped at height {} on success!".format(index, stop_height))

        if stop_height != 0 and current_height >= stop_height + config["ela"]["max_inactivate_rounds"] + 14:
            arbiters_info = controller.middle.service_manager.rpc.get_arbiters_info()
            arbiters_list = arbiters_info["arbiters"]
            print(arbiters_info)
            print(arbiters_list)
            Logger.info("inactive public key: {}".format(inactive_public_key))
            Logger.info("replace public key: {}".format(replace_public_key))
            if replace_public_key in arbiters_list and inactive_public_key not in arbiters_list:
                controller.test_result(test_case, True)
                break
            else:
                controller.test_result(test_case, False)

        #     deposit_address = controller.middle.tx_manager.tx.register_producers_list[1].deposit_address
        #     balance = controller.middle.service_manager.rpc.get_balance_by_address(deposit_address)
        #     Logger.info("[main] The balance of deposit address is {}".format(balance))
        #     if balance == 5000:
        #         Logger.error("The money in the pledge address has not been reduced, exit...")
        #         break
        #     ret = controller.middle.tx_manager.tx.activate_a_producer(
        #         controller.middle.tx_manager.tx.register_producers_list[1]
        #     )
        # if stop_height != 0 and current_height > stop_height + 60:
        #     break
        time.sleep(1)
        controller.discrete_mining_blocks(1)

    controller.terminate_all_process()